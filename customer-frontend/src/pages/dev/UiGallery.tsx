import { FC, useState } from 'react';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Input } from '../../components/ui/Input';
import { Textarea } from '../../components/ui/Textarea';
import { Select } from '../../components/ui/Select';
import { Modal } from '../../components/ui/Modal';
import { Drawer } from '../../components/ui/Drawer';
import { Tabs } from '../../components/ui/Tabs';
import { EmptyState } from '../../components/ui/EmptyState';
import { Skeleton } from '../../components/ui/Skeleton';
import { Avatar } from '../../components/ui/Avatar';
import { Rating } from '../../components/ui/Rating';
import { ToastProvider, useToast } from '../../components/ui/Toast';
import { Accordion } from '../../components/ui/Accordion';
import { ImageUploader } from '../../components/ui/ImageUploader';
import { Search, Bell, Sparkles, Inbox } from 'lucide-react';

const GalleryContent: FC = () => {
  const { showToast } = useToast();
  const [modalOpen, setModalOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('tab1');
  const [rating, setRating] = useState(4);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  return (
    <div className="min-h-screen bg-[#F8FAFC] p-6 lg:p-12 max-w-6xl mx-auto space-y-10">
      <header className="border-b border-slate-200 pb-5">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#2563EB] text-white">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">SmartServe UI Component Gallery</h1>
            <p className="text-sm text-slate-500">Development playground for Phase 2 design primitives</p>
          </div>
        </div>
      </header>

      {/* Buttons */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">1. Buttons</h2>
        <Card className="flex flex-wrap items-center gap-4">
          <Button variant="primary">Primary Button</Button>
          <Button variant="secondary">Secondary Button</Button>
          <Button variant="ghost">Ghost Button</Button>
          <Button variant="danger">Danger Button</Button>
          <Button variant="primary" loading>Loading</Button>
          <Button variant="primary" icon={<Bell className="h-4 w-4" />}>With Icon</Button>
          <Button variant="secondary" size="sm">Small</Button>
          <Button variant="secondary" size="lg">Large</Button>
        </Card>
      </section>

      {/* Badges */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">2. Badges</h2>
        <Card className="flex flex-wrap items-center gap-4">
          <Badge variant="success">Confirmed</Badge>
          <Badge variant="warning">Pending</Badge>
          <Badge variant="danger">Cancelled</Badge>
          <Badge variant="info">In Progress</Badge>
          <Badge variant="neutral">Neutral</Badge>
        </Card>
      </section>

      {/* Form Inputs */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">3. Form Inputs</h2>
        <Card className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input label="Full Name" placeholder="e.g. Pushkar Kanjani" leftIcon={<Search className="h-4 w-4" />} />
          <Input label="Email Address" error="Please enter a valid email address" defaultValue="invalid-email" />
          <Select
            label="Preferred Slot"
            options={[
              { value: 'morning', label: 'Morning (9 AM - 12 PM)' },
              { value: 'afternoon', label: 'Afternoon (12 PM - 4 PM)' },
              { value: 'evening', label: 'Evening (4 PM - 8 PM)' },
            ]}
          />
          <Textarea label="Special Instructions" placeholder="Add optional notes for the service provider..." showCount maxLength={200} value="Handle with care." onChange={() => {}} />
        </Card>
      </section>

      {/* Avatars & Ratings */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">4. Avatars & Ratings</h2>
        <Card className="flex flex-wrap items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <Avatar name="Pushkar Kanjani" size="sm" />
            <Avatar name="Aastha Sharma" size="md" />
            <Avatar name="SmartServe Admin" size="lg" />
          </div>
          <div className="space-y-2">
            <p className="text-sm font-semibold text-slate-700">Interactive Rating: {rating} stars</p>
            <Rating value={rating} interactive onChange={setRating} showValue />
          </div>
        </Card>
      </section>

      {/* Modals, Drawers & Toasts */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">5. Modals, Drawers & Toasts</h2>
        <Card className="flex flex-wrap items-center gap-4">
          <Button variant="secondary" onClick={() => setModalOpen(true)}>Open Modal</Button>
          <Button variant="secondary" onClick={() => setDrawerOpen(true)}>Open Filter Drawer</Button>
          <Button variant="primary" onClick={() => showToast('Booking created successfully!', 'success')}>Trigger Success Toast</Button>
          <Button variant="danger" onClick={() => showToast('Failed to connect to backend', 'error')}>Trigger Error Toast</Button>
        </Card>

        <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Sample Modal Dialog">
          <p className="text-sm text-slate-600">This is a fully accessible focus-trapped modal dialog with ESC key support.</p>
          <div className="mt-6 flex justify-end gap-3">
            <Button variant="secondary" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button variant="primary" onClick={() => setModalOpen(false)}>Confirm</Button>
          </div>
        </Modal>

        <Drawer isOpen={drawerOpen} onClose={() => setDrawerOpen(false)} title="Filter Services">
          <div className="space-y-4">
            <Input label="Search within results" placeholder="Search..." />
            <Select label="Sort By" options={[{ value: 'price', label: 'Price: Low to High' }]} />
            <Button variant="primary" fullWidth onClick={() => setDrawerOpen(false)}>Apply Filters</Button>
          </div>
        </Drawer>
      </section>

      {/* Tabs & Accordion */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">6. Tabs & Accordion</h2>
        <Card className="space-y-6">
          <Tabs
            activeTab={activeTab}
            onChange={setActiveTab}
            items={[
              { id: 'tab1', label: 'Overview', count: 3 },
              { id: 'tab2', label: 'Reviews', count: 12 },
              { id: 'tab3', label: 'FAQs' },
            ]}
          />
          <Accordion
            items={[
              { id: '1', title: 'What is Cash on Delivery?', content: 'You can pay cash directly to the service provider upon service completion.' },
              { id: '2', title: 'How to reschedule a booking?', content: 'Go to your Bookings list, select the active booking, and choose Reschedule.' },
            ]}
          />
        </Card>
      </section>

      {/* Empty States & Skeletons */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">7. Empty States & Skeletons</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <EmptyState icon={<Inbox className="h-6 w-6" />} title="No Bookings Found" description="You have not placed any service bookings yet." actionLabel="Browse Services" onAction={() => {}} />
          <Card className="space-y-3">
            <Skeleton variant="text" width="60%" />
            <Skeleton variant="rectangular" height={100} />
            <div className="flex gap-3">
              <Skeleton variant="circular" width={40} height={40} />
              <div className="flex-1 space-y-2">
                <Skeleton variant="text" />
                <Skeleton variant="text" width="80%" />
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Image Uploader */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-slate-800">8. Image Uploader</h2>
        <Card>
          <ImageUploader files={uploadedFiles} onChange={setUploadedFiles} />
        </Card>
      </section>
    </div>
  );
};

export const UiGallery: FC = () => {
  return (
    <ToastProvider>
      <GalleryContent />
    </ToastProvider>
  );
};

export default UiGallery;
