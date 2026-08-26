from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.provider import Provider

def calculate_provider_rankings(db: Session) -> List[Dict[str, Any]]:
    """Compute provider rankings using composite score formula:
       Score = (reliability * 0.4) + (acceptance_rate * 0.3) + (on_time_rate * 0.2) - (cancellation_rate * 0.1)
    """
    providers = db.query(Provider).all()
    ranked_list = []

    for p in providers:
        rel = float(getattr(p, 'reliability_score', 98.0))
        acc = float(getattr(p, 'acceptance_rate', 95.0))
        ont = float(getattr(p, 'on_time_rate', 99.0))
        cnc = float(getattr(p, 'cancellation_rate', 2.0))

        composite_score = round((rel * 0.4) + (acc * 0.3) + (ont * 0.2) - (cnc * 0.1), 2)

        ranked_list.append({
            "provider_user_id": str(p.user_id),
            "full_name": p.full_name,
            "category": getattr(p, 'category', 'General'),
            "reliability_score": rel,
            "acceptance_rate": acc,
            "on_time_rate": ont,
            "composite_rank_score": composite_score,
            "rank_tier": "Tier 1 — Elite" if composite_score >= 85.0 else "Tier 2 — Preferred"
        })

    # Sort descending by composite rank score
    ranked_list.sort(key=lambda x: x["composite_rank_score"], reverse=True)
    for idx, item in enumerate(ranked_list, start=1):
        item["rank_position"] = idx

    return ranked_list

def estimate_provider_eta(provider_user_id: str, distance_km: float = 5.2) -> Dict[str, Any]:
    """Estimate provider ETA based on distance, traffic multiplier, and prep buffer."""
    traffic_multiplier = 1.25 # Peak traffic adjustment factor
    base_speed_kmh = 30.0 # Average city driving speed
    travel_minutes = round((distance_km / base_speed_kmh) * 60 * traffic_multiplier, 1)
    prep_buffer_minutes = 10.0
    total_eta_minutes = round(travel_minutes + prep_buffer_minutes)

    return {
        "provider_user_id": provider_user_id,
        "distance_km": distance_km,
        "traffic_multiplier": traffic_multiplier,
        "travel_minutes": travel_minutes,
        "prep_buffer_minutes": prep_buffer_minutes,
        "total_eta_minutes": total_eta_minutes,
        "estimated_arrival_window": f"{total_eta_minutes - 5}-{total_eta_minutes + 10} mins"
    }
