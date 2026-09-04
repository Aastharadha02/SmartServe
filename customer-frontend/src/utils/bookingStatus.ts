export type BookingStatus =
  | 'Requested'
  | 'Assigned'
  | 'Accepted'
  | 'Started'
  | 'Completed'
  | 'Cancelled'
  | 'Rejected'
  | 'Expired';

export interface BookingStatusConfig {
  label: string;
  variant: 'success' | 'warning' | 'danger' | 'info' | 'neutral';
  description: string;
}

export const statusConfigMap: Record<BookingStatus, BookingStatusConfig> = {
  Requested: {
    label: 'Requested',
    variant: 'warning',
    description: 'Awaiting provider assignment',
  },
  Assigned: {
    label: 'Provider Assigned',
    variant: 'info',
    description: 'Provider has been assigned to your request',
  },
  Accepted: {
    label: 'Accepted',
    variant: 'info',
    description: 'Provider confirmed the appointment',
  },
  Started: {
    label: 'In Progress',
    variant: 'info',
    description: 'Service has started at your location',
  },
  Completed: {
    label: 'Completed',
    variant: 'success',
    description: 'Service completed successfully',
  },
  Cancelled: {
    label: 'Cancelled',
    variant: 'danger',
    description: 'Booking was cancelled',
  },
  Rejected: {
    label: 'Declined',
    variant: 'danger',
    description: 'Request was declined by provider',
  },
  Expired: {
    label: 'Expired',
    variant: 'neutral',
    description: 'Request timed out before assignment',
  },
};

export const getBookingStatusConfig = (status: BookingStatus): BookingStatusConfig => {
  return statusConfigMap[status] || {
    label: status,
    variant: 'neutral',
    description: '',
  };
};
