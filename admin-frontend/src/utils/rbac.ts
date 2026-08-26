import type { SessionAdminInfo } from '../api/admins';

/**
 * Single central RBAC permission evaluator.
 * Evaluates whether an authenticated admin has permission to perform a specific action.
 */
export function hasPermission(
  session: SessionAdminInfo | null,
  requiredPermission: string
): boolean {
  if (!session) return false;

  // Super Admin bypasses all single-action restrictions
  if (session.role === 'super_admin' || session.role_name === 'super_admin') {
    return true;
  }

  const perms = session.permissions || [];

  // Direct match (e.g. 'catalog:edit', 'bookings:manage')
  if (perms.includes(requiredPermission)) {
    return true;
  }

  const [modulePrefix, actionType] = requiredPermission.split(':');

  // 'module:manage' grants all actions within that module
  if (perms.includes(`${modulePrefix}:manage`)) {
    return true;
  }

  // 'module:edit' grants modification actions (create, edit, delete, save, status)
  if (
    actionType &&
    ['create', 'edit', 'delete', 'save', 'update', 'status'].includes(actionType) &&
    perms.includes(`${modulePrefix}:edit`)
  ) {
    return true;
  }

  return false;
}
