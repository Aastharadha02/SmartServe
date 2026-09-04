/**
 * SmartServe Shared Service & Category Photography
 * SINGLE SOURCE OF TRUTH: Directly imported and re-exported from Admin Catalog Master
 * Source: admin-frontend/src/utils/serviceImages.ts
 *
 * There is NO independently maintained duplicate photography dictionary here.
 * Customer consumes the EXACT same image mappings and resolver as Admin.
 */

export * from '../../../admin-frontend/src/utils/serviceImages';
import {
  getServiceImage as adminGetServiceImage,
  DEFAULT_SERVICE_IMAGE
} from '../../../admin-frontend/src/utils/serviceImages';

export function getCategoryImageUrl(categoryName?: string | null): string {
  if (!categoryName) return DEFAULT_SERVICE_IMAGE;
  return adminGetServiceImage(categoryName);
}

export function getServiceImage(
  categoryOrObjOrName?: any,
  subcategoryOrCategory?: any,
  serviceName?: string
): string {
  if (typeof categoryOrObjOrName === 'object' && categoryOrObjOrName !== null) {
    const s = categoryOrObjOrName;
    if (s.image_url && !s.image_url.includes('photo-1621905251189-08b45d6a269e')) {
      return s.image_url;
    }
    return adminGetServiceImage(s.category, s.subcategory, s.name || s.service_name);
  }
  return adminGetServiceImage(categoryOrObjOrName, subcategoryOrCategory, serviceName);
}
