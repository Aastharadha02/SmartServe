import asyncio
import json
import httpx
import websockets
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"
WS_URL = "ws://127.0.0.1:8000/ws/stream"

async def run_e2e_test():
    print("=" * 70)
    print("SMARTSERVE LIVE-TRACKING, ROAD ROUTING & OTP STATE MACHINE E2E TEST")
    print("=" * 70)

    results = {}

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Login as Admin
        print("\n1. Logging in as Admin...")
        admin_login = await client.post("/auth/login", json={
            "email": "admin@smartserve.com",
            "password": "AdminPassword123!"
        })
        assert admin_login.status_code == 200, f"Admin login failed: {admin_login.text}"
        admin_token = admin_login.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print("  -> Admin logged in successfully.")

        # 2. Login as Provider
        print("\n2. Logging in as Provider...")
        prov_login = await client.post("/auth/login", json={
            "email": "rajesh.sharma@smartserve.com",
            "password": "ProviderPass123!"
        })
        assert prov_login.status_code == 200, f"Provider login failed: {prov_login.text}"
        prov_data = prov_login.json()
        prov_token = prov_data["access_token"]
        prov_user_id = prov_data["user_id"]
        prov_headers = {"Authorization": f"Bearer {prov_token}"}
        print(f"  -> Provider logged in (User ID: {prov_user_id}).")

        # 3. Login as Customer
        print("\n3. Logging in as Customer...")
        cust_login = await client.post("/auth/login", json={
            "email": "ananya.rao@example.com",
            "password": "CustomerPass123!"
        })
        assert cust_login.status_code == 200, f"Customer login failed: {cust_login.text}"
        cust_token = cust_login.json()["access_token"]
        cust_headers = {"Authorization": f"Bearer {cust_token}"}
        print("  -> Customer logged in.")

        # 4. Fetch catalog service matching provider
        print("\n4. Fetching catalog service matching provider...")
        services_res = await client.get("/services/882b49bd-c684-4725-9608-3edb72ab9b82")
        assert services_res.status_code == 200
        service = services_res.json()
        service_id = service["id"]
        title = service.get("name") or service.get("title") or "Service"
        print(f"  -> Selected Service: {title} (ID: {service_id}, Category: {service.get('category')})")

        # 5. Customer creates or finds active Requested booking assigned to provider
        print("\n5. Customer finding or creating booking...")
        bookings_res = await client.get("/customer/bookings", headers=cust_headers)
        requested_list = [
            b for b in bookings_res.json()
            if b.get("status", "").lower() == "requested" and (
                b.get("provider_id") == str(prov_user_id) or "rajesh" in (b.get("provider_name") or "").lower()
            )
        ]
        if requested_list:
            booking = requested_list[0]
            booking_id = booking["id"]
            print(f"  -> Using existing Requested booking: {booking.get('booking_reference', booking_id)} (ID: {booking_id})")
        else:
            create_booking_res = await client.post("/customer/bookings", json={
                "service_id": str(service_id),
                "scheduled_date": "2026-10-10",
                "scheduled_time": "05:00 PM",
                "address_line1": "104 Emerald Heights, Indiranagar, Bengaluru",
                "city": "Bengaluru",
                "pincode": "560038",
                "provider_id": str(prov_user_id),
                "notes": "E2E live map test with road routing and start OTP"
            }, headers=cust_headers)
            assert create_booking_res.status_code in [200, 201], f"Create booking failed: {create_booking_res.text}"
            booking = create_booking_res.json()
            booking_id = booking["id"]
            print(f"  -> Booking created: {booking['booking_reference']} (ID: {booking_id}), Status: {booking['status']}")
        results["Booking Creation"] = "PASS"

        # WebSocket listener to capture live broadcast events
        ws_received_events = []
        async def listen_ws():
            ws_uri = f"{WS_URL}?channels=booking_{booking_id},admin_booking_{booking_id},bookings"
            try:
                async with websockets.connect(ws_uri) as ws:
                    while True:
                        msg = await ws.recv()
                        data = json.loads(msg)
                        if data.get("type") not in ["pong", "CONNECTION_ESTABLISHED", "SUBSCRIBED"]:
                            ws_received_events.append(data)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                pass

        ws_task = asyncio.create_task(listen_ws())
        await asyncio.sleep(0.5)

        # 6. Provider accepts the booking
        print("\n6. Provider accepting booking...")
        accept_res = await client.post(f"/providers/me/bookings/{booking_id}/accept", headers=prov_headers)
        assert accept_res.status_code == 200, f"Provider accept failed: {accept_res.text}"
        assert accept_res.json()["status"].lower() == "accepted", f"Expected Accepted, got {accept_res.json()['status']}"
        print("  -> Booking status: ACCEPTED")
        results["Provider Accept (ACCEPTED)"] = "PASS"

        # 7. Provider starts trip -> ON_THE_WAY
        print("\n7. Provider starting trip (ON_THE_WAY)...")
        otw_res = await client.patch(f"/providers/me/bookings/{booking_id}/status", json={
            "status": "On The Way"
        }, headers=prov_headers)
        assert otw_res.status_code == 200, f"On The Way failed: {otw_res.text}"
        assert otw_res.json()["status"].lower() == "on the way"
        print("  -> Booking status: ON THE WAY")
        results["Provider Trip (ON_THE_WAY)"] = "PASS"

        # 8. Provider sends live GPS updates
        print("\n8. Transmitting real-time GPS coordinate updates from provider...")
        gps_path = [
            {"latitude": 12.971598, "longitude": 77.594566, "heading": 42.0, "speed": 21.0, "accuracy": 6.5},
            {"latitude": 12.973800, "longitude": 77.598400, "heading": 65.0, "speed": 24.5, "accuracy": 5.0},
            {"latitude": 12.976500, "longitude": 77.602200, "heading": 78.0, "speed": 27.0, "accuracy": 4.2},
        ]

        for i, pt in enumerate(gps_path, 1):
            gps_payload = {
                "booking_id": booking_id,
                "latitude": pt["latitude"],
                "longitude": pt["longitude"],
                "heading": pt["heading"],
                "speed": pt["speed"],
                "accuracy": pt["accuracy"]
            }
            gps_res = await client.post("/providers/me/location", json=gps_payload, headers=prov_headers)
            assert gps_res.status_code == 200, f"GPS update {i} failed: {gps_res.text}"
            print(f"  -> GPS update #{i}: lat={pt['latitude']}, lng={pt['longitude']}, heading={pt['heading']}°, speed={pt['speed']} km/h")
            await asyncio.sleep(0.3)

        results["Provider Live GPS Updates"] = "PASS"

        # 9. Verify Customer Live Location Endpoint
        print("\n9. Customer retrieving live provider tracking & location...")
        cust_loc_res = await client.get(f"/customer/bookings/{booking_id}/location", headers=cust_headers)
        assert cust_loc_res.status_code == 200, f"Customer location query failed: {cust_loc_res.text}"
        cust_loc = cust_loc_res.json()
        assert cust_loc["provider_location"] is not None
        assert abs(cust_loc["provider_location"]["latitude"] - 12.976500) < 0.0001
        print(f"  -> Customer received live provider position: lat={cust_loc['provider_location']['latitude']}, heading={cust_loc['provider_location']['heading']}")
        results["Customer Live Tracking"] = "PASS"

        # 10. Verify Admin Live Location Monitoring Endpoint
        print("\n10. Admin retrieving live provider tracking & trip telemetry...")
        admin_loc_res = await client.get(f"/admin/bookings/{booking_id}/location", headers=admin_headers)
        assert admin_loc_res.status_code == 200, f"Admin location query failed: {admin_loc_res.text}"
        admin_loc = admin_loc_res.json()
        assert admin_loc["provider_location"] is not None
        assert abs(admin_loc["provider_location"]["latitude"] - 12.976500) < 0.0001
        print(f"  -> Admin received live location: lat={admin_loc['provider_location']['latitude']}, speed={admin_loc['provider_location']['speed']} km/h")
        results["Admin Live Monitoring"] = "PASS"

        # 11. Security & RBAC: Customer and Provider cannot access Admin Location endpoint
        print("\n11. Testing RBAC on Admin Live Monitoring endpoint...")
        cust_blocked = await client.get(f"/admin/bookings/{booking_id}/location", headers=cust_headers)
        assert cust_blocked.status_code in [401, 403], f"Security leak! Customer received status {cust_blocked.status_code}"
        prov_blocked = await client.get(f"/admin/bookings/{booking_id}/location", headers=prov_headers)
        assert prov_blocked.status_code in [401, 403], f"Security leak! Provider received status {prov_blocked.status_code}"
        print("  -> RBAC correctly enforced: Customer and Provider forbidden (403).")
        results["Location RBAC Security"] = "PASS"

        # 12. Provider reaches destination -> ARRIVED
        print("\n12. Provider marking ARRIVED...")
        arrived_res = await client.patch(f"/providers/me/bookings/{booking_id}/status", json={
            "status": "Arrived"
        }, headers=prov_headers)
        assert arrived_res.status_code == 200, f"Mark arrived failed: {arrived_res.text}"
        assert arrived_res.json()["status"].lower() == "arrived"
        print("  -> Booking status: ARRIVED")
        results["Provider Arrived State"] = "PASS"

        # 13. Customer sees start OTP, Provider response MASKS OTP
        print("\n13. Verifying Start OTP generation and Provider response masking...")
        cust_detail_res = await client.get(f"/customer/bookings/{booking_id}", headers=cust_headers)
        assert cust_detail_res.status_code == 200
        cust_b = cust_detail_res.json()
        otp = cust_b.get("otp_code")
        assert otp is not None and len(otp) == 4 and otp.isdigit(), f"Invalid OTP format: {otp}"
        print(f"  -> Customer sees 4-digit Service Start OTP: {otp}")

        prov_detail_res = await client.get(f"/providers/me/bookings/{booking_id}", headers=prov_headers)
        assert prov_detail_res.status_code == 200
        prov_b = prov_detail_res.json()
        assert prov_b.get("otp_code") is None, f"Security leak! Provider sees OTP: {prov_b.get('otp_code')}"
        print("  -> Confirmed: Provider API response masks otp_code as None.")
        results["Start OTP Generation & Provider Masking"] = "PASS"

        # 14. Invalid OTP rejection: Provider attempts START with invalid OTP -> MUST FAIL
        print("\n14. Testing START rejection with invalid OTP (0000)...")
        bad_start_res = await client.post(f"/providers/me/bookings/{booking_id}/start", json={
            "otp_code": "0000" if otp != "0000" else "9999"
        }, headers=prov_headers)
        assert bad_start_res.status_code == 400, f"Expected 400 Bad Request, got {bad_start_res.status_code}: {bad_start_res.text}"
        print(f"  -> Backend rejected invalid OTP: {bad_start_res.json()['detail']}")
        results["Invalid OTP Blocked"] = "PASS"

        # 15. Valid OTP verification: Provider enters customer OTP -> MUST SUCCEED
        print(f"\n15. Starting service with customer OTP ({otp})...")
        good_start_res = await client.post(f"/providers/me/bookings/{booking_id}/start", json={
            "otp_code": otp
        }, headers=prov_headers)
        assert good_start_res.status_code == 200, f"Start service failed: {good_start_res.text}"
        assert good_start_res.json()["status"].lower() == "started"
        print("  -> Service started successfully (status: STARTED).")
        results["Service Started with OTP"] = "PASS"

        # 16. Verify single-use OTP consumed
        print("\n16. Verifying single-use OTP consumed from database...")
        post_start_cust = await client.get(f"/customer/bookings/{booking_id}", headers=cust_headers)
        assert post_start_cust.json().get("otp_code") is None, "OTP was not invalidated in DB after verification!"
        print("  -> Confirmed: otp_code is now None in database.")
        results["Single-use OTP Consumed"] = "PASS"

        # 17. Provider completes service WITHOUT asking for OTP
        print("\n17. Provider completing service (no OTP required at completion)...")
        complete_res = await client.post(f"/providers/me/bookings/{booking_id}/complete", json={
            "notes": "Service satisfactorily completed"
        }, headers=prov_headers)
        assert complete_res.status_code == 200, f"Complete service failed: {complete_res.text}"
        assert complete_res.json()["status"].lower() == "completed"
        print("  -> Service completed successfully (status: COMPLETED).")
        results["Service Completed (No OTP)"] = "PASS"

        # 18. Location updates stopped after completion
        print("\n18. Verifying location updates stopped post-completion...")
        post_complete_gps = await client.post("/providers/me/location", json={
            "booking_id": booking_id,
            "latitude": 12.977000,
            "longitude": 77.603000
        }, headers=prov_headers)
        assert post_complete_gps.status_code == 400, f"Expected 400 for post-completion GPS update, got {post_complete_gps.status_code}"
        print(f"  -> GPS update rejected as required: {post_complete_gps.json()['detail']}")
        results["Location Updates Stopped Post-Completion"] = "PASS"

        # 19. WebSocket events verification
        await asyncio.sleep(0.5)
        ws_task.cancel()
        print(f"\n19. Real-time WebSocket events captured: {len(ws_received_events)}")
        event_types = [ev.get("type") for ev in ws_received_events]
        for t in event_types:
            print(f"  - WS Event: {t}")
        assert "PROVIDER_LOCATION_UPDATED" in event_types, "Missing PROVIDER_LOCATION_UPDATED in WebSocket stream"
        assert "BOOKING_STARTED" in event_types, "Missing BOOKING_STARTED in WebSocket stream"
        assert "BOOKING_COMPLETED" in event_types, "Missing BOOKING_COMPLETED in WebSocket stream"
        results["WebSocket Real-time Broadcast"] = "PASS"

    print("\n" + "=" * 70)
    print("ALL E2E LIFECYCLE TESTS PASSED FACTUALLY!")
    print("=" * 70)
    for k, v in results.items():
        print(f"  {k:42}: {v}")

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
