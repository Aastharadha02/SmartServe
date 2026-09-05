import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search, 
  LayoutGrid, 
  List, 
  ChevronRight, 
  Loader2, 
  RefreshCw, 
  AlertCircle,
  CheckCircle2,
  FolderTree,
  Plus,
  X,
  Check,
  FileSpreadsheet,
  Upload,
  LogIn
} from 'lucide-react';
import { 
  getCatalogServices, 
  createCatalogService, 
  exportCatalogExcel, 
  importCatalogExcel, 
  previewImportCatalogExcel,
  generateAiMetadata 
} from '../../../api/catalog';
import type { ServiceItem } from '../../../api/catalog';
import { getCategoryIcon } from '../../../utils/catalogIcons';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';
import { getServiceImage, formatCategoryDisplayName, DEFAULT_SERVICE_IMAGE } from '../../../utils/serviceImages';

export const CategoryListView: React.FC = () => {
  const navigate = useNavigate();
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Add New Service Modal State
  const [isCreateOpen, setIsCreateOpen] = useState<boolean>(false);
  const [formName, setFormName] = useState<string>('');
  const [formCategory, setFormCategory] = useState<string>('');
  const [formSubcategory, setFormSubcategory] = useState<string>('');
  const [formBasePrice, setFormBasePrice] = useState<number>(499);
  const [formMaxSurge, setFormMaxSurge] = useState<number>(0.5);
  const [formMaxDiscount, setFormMaxDiscount] = useState<number>(0.3);
  const [formIsActive, setFormIsActive] = useState<boolean>(true);
  const [createLoading, setCreateLoading] = useState<boolean>(false);
  const [createError, setCreateError] = useState<string | null>(null);

  // Excel States
  const [exportLoading, setExportLoading] = useState<boolean>(false);
  const [importLoading, setImportLoading] = useState<boolean>(false);

  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  const canEditCatalog = hasPermission(adminSession, 'catalog:edit') || hasPermission(adminSession, 'catalog:manage');
  const canCreateCatalog = hasPermission(adminSession, 'catalog:create') || canEditCatalog;
  const canImportCatalog = hasPermission(adminSession, 'catalog:import') || hasPermission(adminSession, 'catalog:manage');
  const canExportCatalog = hasPermission(adminSession, 'catalog:export') || hasPermission(adminSession, 'catalog:manage') || hasPermission(adminSession, 'insights:view');

  const showToast = (text: string, type: 'success' | 'warning' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 5000);
  };

  const fetchCatalogData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCatalogServices();
      setServices(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load service categories from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCatalogData();
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});
  }, []);

  // Helper to extract natural category ordering from database prefix
  const getCategoryOrder = (catName: string): number => {
    const match = catName.match(/^(\d+)\./);
    return match ? parseInt(match[1], 10) : 999;
  };

  // Aggregate Category Cards from backend services
  const categorySummaries = useMemo(() => {
    const map = new Map<string, { subcategories: Set<string>; total: number; active: number }>();

    services.forEach((s) => {
      if (!map.has(s.category)) {
        map.set(s.category, { subcategories: new Set(), total: 0, active: 0 });
      }
      const item = map.get(s.category)!;
      item.subcategories.add(s.subcategory);
      item.total += 1;
      if (s.is_active) item.active += 1;
    });

    const result: Array<{
      name: string;
      displayName: string;
      subcategoriesCount: number;
      serviceCount: number;
      activeCount: number;
      order: number;
    }> = [];

    map.forEach((val, name) => {
      result.push({
        name,
        displayName: formatCategoryDisplayName(name),
        subcategoriesCount: val.subcategories.size,
        serviceCount: val.total,
        activeCount: val.active,
        order: getCategoryOrder(name),
      });
    });

    // Preserve natural category order (1, 2, ..., 14)
    return result.sort((a, b) => a.order - b.order || a.displayName.localeCompare(b.displayName));
  }, [services]);

  const filteredCategories = useMemo(() => {
    return categorySummaries.filter((cat) => {
      const matchesSearch = 
        cat.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        cat.displayName.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = !statusFilter || 
        (statusFilter === 'active' && cat.activeCount > 0) ||
        (statusFilter === 'inactive' && cat.activeCount < cat.serviceCount);
      return matchesSearch && matchesStatus;
    });
  }, [categorySummaries, searchTerm, statusFilter]);

  // Handle New Service Creation + Non-blocking AI Metadata Trigger
  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreateError(null);
    setCreateLoading(true);

    let createdService: ServiceItem | null = null;
    try {
      // 1. Create service in backend
      createdService = await createCatalogService({
        name: formName,
        category: formCategory,
        subcategory: formSubcategory,
        base_price: formBasePrice,
        max_demand_increase: formMaxSurge,
        max_discount: formMaxDiscount,
        is_active: formIsActive,
      });

      setServices((prev) => [createdService!, ...prev]);
      setIsCreateOpen(false);
      showToast(`Service '${createdService.name}' created successfully!`, 'success');

      // 2. Non-blocking AI Metadata trigger
      try {
        await generateAiMetadata(createdService.id);
        showToast(`AI metadata generated automatically for '${createdService.name}'!`, 'success');
      } catch (aiErr) {
        showToast(`Service created, but AI content generation timed out. You can trigger AI metadata anytime in Service Editor.`, 'warning');
      }

      // Navigate to Level 4 editor
      navigate(`/admin/catalog/service/${createdService.id}`);
    } catch (err: any) {
      setCreateError(err.response?.data?.detail || 'Failed to create new service item.');
    } finally {
      setCreateLoading(false);
    }
  };

  // Excel Export Handler
  const handleExportExcel = async () => {
    setExportLoading(true);
    try {
      await exportCatalogExcel();
      showToast('Catalog exported as XLSX spreadsheet.', 'success');
    } catch (err: any) {
      showToast('Failed to export catalog spreadsheet.', 'error');
    } finally {
      setExportLoading(false);
    }
  };

  // Pre-Import Preview Modal States
  const [importFile, setImportFile] = useState<File | null>(null);
  const [previewData, setPreviewData] = useState<any | null>(null);
  const [previewModalOpen, setPreviewModalOpen] = useState<boolean>(false);
  const [confirmImportLoading, setConfirmImportLoading] = useState<boolean>(false);

  // Excel File Select -> Triggers Pre-Import Validation Preview
  const handleImportExcel = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImportLoading(true);
    try {
      const data = await previewImportCatalogExcel(file);
      setPreviewData(data);
      setImportFile(file);
      setPreviewModalOpen(true);
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Excel validation preview failed.', 'error');
    } finally {
      setImportLoading(false);
      e.target.value = '';
    }
  };

  // Final Import Confirmation Handler
  const handleConfirmImport = async () => {
    if (!importFile) return;
    setConfirmImportLoading(true);
    try {
      const res = await importCatalogExcel(importFile);
      showToast(`Spreadsheet imported: ${res.inserted} inserted, ${res.updated} updated.`, 'success');
      setPreviewModalOpen(false);
      setImportFile(null);
      setPreviewData(null);
      fetchCatalogData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Excel import failed.', 'error');
    } finally {
      setConfirmImportLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-medium text-slate-600">Loading SmartServe Service Categories...</p>
      </div>
    );
  }

  if (error) {
    const isAuthError =
      error.toLowerCase().includes('admin role') ||
      error.toLowerCase().includes('forbidden') ||
      error.toLowerCase().includes('unauthorized');

    return (
      <div className="max-w-2xl mx-auto my-12 p-6 bg-white border border-red-200 rounded-2xl shadow-sm text-center space-y-4">
        <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Failed to Load Catalog Categories</h3>
        <p className="text-xs text-slate-600 max-w-md mx-auto">{error}</p>
        <div className="flex items-center justify-center gap-3 pt-2">
          {isAuthError ? (
            <button
              onClick={() => {
                localStorage.removeItem('smartserve_token');
                localStorage.removeItem('smartserve_user');
                window.location.href = '/login';
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white rounded-xl text-xs font-semibold shadow-sm transition-colors"
            >
              <LogIn className="w-3.5 h-3.5" />
              <span>Log In as Admin</span>
            </button>
          ) : (
            <button
              onClick={fetchCatalogData}
              className="inline-flex items-center gap-2 px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white rounded-xl text-xs font-semibold shadow-sm transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry Connection</span>
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-[#1F2A1E]">
      {/* Toast Notification */}
      {toastMessage && (
        <div className={`fixed top-20 right-8 z-50 flex items-center gap-3 px-4 py-3 text-white rounded-2xl shadow-lg border text-xs font-semibold animate-in fade-in ${
          toastMessage.type === 'success' ? 'bg-[#1F2A1E] border-[#2F5233]' :
          toastMessage.type === 'warning' ? 'bg-amber-900 border-amber-700' : 'bg-red-900 border-red-700'
        }`}>
          <CheckCircle2 className={`w-4 h-4 ${toastMessage.type === 'success' ? 'text-emerald-400' : 'text-amber-400'}`} />
          <span>{toastMessage.text}</span>
        </div>
      )}

      {/* Level 1 Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-xs">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-serif text-[#1F2A1E] tracking-tight">Service Catalog Categories</h1>
            <span className="text-xs font-bold text-[#2F5233] bg-[#F2EDE1] px-3 py-1 rounded-full border border-[#E5DEC9]">
              {categorySummaries.length} Categories
            </span>
          </div>
          <p className="text-sm md:text-base text-[#1F2A1E]/65 font-medium mt-1">
            Explore 14 main service categories, subcategories, pricing, and AI-assisted content guidelines
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          {canExportCatalog ? (
            <button
              onClick={handleExportExcel}
              disabled={exportLoading}
              className="flex items-center gap-2 px-3.5 py-2.5 bg-white hover:bg-[#F2EDE1] text-emerald-800 font-semibold text-xs rounded-xl border border-emerald-200 transition-colors disabled:opacity-50 cursor-pointer shadow-2xs"
            >
              {exportLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileSpreadsheet className="w-4 h-4 text-emerald-700" />}
              <span>Export XLSX</span>
            </button>
          ) : (
            <button
              disabled
              title="Exporting catalog data requires 'catalog:export' or 'catalog:manage' permission."
              className="flex items-center gap-2 px-3.5 py-2.5 bg-[#F2EDE1] text-[#1F2A1E]/40 font-semibold text-xs rounded-xl border border-[#E5DEC9] cursor-not-allowed opacity-60"
            >
              <FileSpreadsheet className="w-4 h-4 text-[#1F2A1E]/40" />
              <span>Export (Disabled)</span>
            </button>
          )}

          {canImportCatalog ? (
            <label className="flex items-center gap-2 px-3.5 py-2.5 bg-white hover:bg-[#F2EDE1] text-[#1F2A1E] font-semibold text-xs rounded-xl border border-[#E5DEC9] transition-colors cursor-pointer shadow-2xs">
              {importLoading ? <Loader2 className="w-4 h-4 animate-spin text-[#2F5233]" /> : <Upload className="w-4 h-4 text-[#1F2A1E]/60" />}
              <span>Import XLSX</span>
              <input type="file" accept=".xlsx, .xls" onChange={handleImportExcel} className="hidden" />
            </label>
          ) : (
            <button
              disabled
              title="Importing catalog data requires 'catalog:import' or 'catalog:manage' permission."
              className="flex items-center gap-2 px-3.5 py-2.5 bg-[#F2EDE1] text-[#1F2A1E]/40 font-semibold text-xs rounded-xl border border-[#E5DEC9] cursor-not-allowed opacity-60"
            >
              <Upload className="w-4 h-4 text-[#1F2A1E]/40" />
              <span>Import (Disabled)</span>
            </button>
          )}

          {canCreateCatalog ? (
            <button
              onClick={() => {
                setFormName('');
                setFormCategory(categorySummaries[0]?.name || 'Home Cleaning');
                setFormSubcategory('General Maintenance');
                setFormBasePrice(499);
                setIsCreateOpen(true);
              }}
              className="flex items-center gap-2 px-4 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-semibold text-xs rounded-xl shadow-xs transition-colors cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Add New Service</span>
            </button>
          ) : (
            <button
              disabled
              title="Creating new catalog services requires 'catalog:manage' or 'catalog:create' permission."
              className="flex items-center gap-2 px-4 py-2.5 bg-[#F2EDE1] text-[#1F2A1E]/40 font-semibold text-xs rounded-xl cursor-not-allowed opacity-70 border border-[#E5DEC9]"
            >
              <Plus className="w-4 h-4 text-[#1F2A1E]/40" />
              <span>Add Service (Disabled)</span>
            </button>
          )}
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-xs">
        <div className="relative flex-1 w-full max-w-md">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/40" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search categories..."
            className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20"
          >
            <option value="">All Categories</option>
            <option value="active">Active Only</option>
            <option value="inactive">Contains Inactive Services</option>
          </select>

          <div className="flex items-center bg-[#F2EDE1] p-1 rounded-xl border border-[#E5DEC9]">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg transition-colors cursor-pointer ${viewMode === 'grid' ? 'bg-white text-[#2F5233] shadow-xs' : 'text-[#1F2A1E]/60 hover:text-[#1F2A1E]'}`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg transition-colors cursor-pointer ${viewMode === 'list' ? 'bg-white text-[#2F5233] shadow-xs' : 'text-[#1F2A1E]/60 hover:text-[#1F2A1E]'}`}
              title="List View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Category Grid or List Render */}
      {filteredCategories.length === 0 ? (
        <div className="py-16 text-center bg-white rounded-3xl border border-[#E5DEC9] shadow-xs space-y-3">
          <FolderTree className="w-10 h-10 text-[#1F2A1E]/40 mx-auto" />
          <h3 className="text-base font-bold text-[#1F2A1E]">No Categories Found</h3>
          <p className="text-xs text-[#1F2A1E]/60 font-medium">No catalog categories match your search filters.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredCategories.map((cat) => {
            const catImage = getServiceImage(cat.name);
            return (
              <div
                key={cat.name}
                onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(cat.name)}`)}
                className="group bg-white rounded-3xl border border-[#E5DEC9] shadow-xs hover:shadow-md hover:border-[#2F5233]/40 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
              >
                {/* Category Photography Cover */}
                <div className="relative w-full h-44 bg-[#F2EDE1] overflow-hidden">
                  <img
                    src={catImage}
                    alt={cat.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    loading="lazy"
                    onError={(e) => {
                      e.currentTarget.onerror = null;
                      e.currentTarget.src = DEFAULT_SERVICE_IMAGE;
                    }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-[#1F2A1E]/80 via-[#1F2A1E]/30 to-transparent"></div>

                  <div className="absolute bottom-3 left-4 right-4 flex items-end justify-between">
                    <div>
                      <h3 className="text-lg font-serif font-bold text-white tracking-tight drop-shadow-xs">
                        {cat.displayName}
                      </h3>
                      <p className="text-xs text-[#FAF7F0]/90 font-medium">
                        {cat.subcategoriesCount} Subcategories • {cat.serviceCount} Services
                      </p>
                    </div>

                    <div className="w-8 h-8 rounded-full bg-white/20 backdrop-blur-xs text-white flex items-center justify-center group-hover:bg-[#2F5233] transition-colors">
                      <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                    </div>
                  </div>
                </div>

                <div className="p-4 sm:p-5 flex items-center justify-between text-xs">
                  <span className="inline-flex items-center gap-1.5 text-emerald-800 font-bold bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                    <span>{cat.activeCount} Active</span>
                  </span>

                  <span className="font-bold text-[#2F5233] group-hover:underline flex items-center gap-1">
                    <span>Explore</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-[#E5DEC9] shadow-xs overflow-hidden">
          <div className="divide-y divide-[#E5DEC9]">
            {filteredCategories.map((cat) => {
              const IconComponent = getCategoryIcon(cat.name);
              return (
                <div
                  key={cat.name}
                  onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(cat.name)}`)}
                  className="p-4 flex items-center justify-between hover:bg-[#FAF7F0] transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-xl bg-[#F2EDE1] text-[#2F5233] flex items-center justify-center border border-[#E5DEC9]">
                      <IconComponent className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-[#1F2A1E] font-serif">{cat.displayName}</h3>
                      <p className="text-xs text-[#1F2A1E]/60">
                        {cat.subcategoriesCount} Subcategories • {cat.serviceCount} Services
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <span className="text-xs font-semibold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                      {cat.activeCount} Active
                    </span>
                    <ChevronRight className="w-4 h-4 text-[#1F2A1E]/40" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Add New Service Modal */}
      {isCreateOpen && (
        <div className="fixed inset-0 z-50 bg-[#1F2A1E]/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] overflow-hidden animate-in fade-in">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#E5DEC9] bg-[#FAF7F0]">
              <h3 className="font-bold font-serif text-[#1F2A1E] text-base">Add New Service Item</h3>
              <button onClick={() => setIsCreateOpen(false)} className="text-[#1F2A1E]/40 hover:text-[#1F2A1E] cursor-pointer">
                <X className="w-5 h-5" />
              </button>
            </div>

            {createError && (
              <div className="mx-6 mt-4 p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                <span>{createError}</span>
              </div>
            )}

            <form onSubmit={handleCreateSubmit} className="p-6 space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-[#1F2A1E] mb-1">Service Name</label>
                <input
                  type="text"
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                  placeholder="e.g. Deep Home Haircut & Styling"
                  className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 font-semibold"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-[#1F2A1E] mb-1">Category</label>
                  <input
                    type="text"
                    value={formCategory}
                    onChange={(e) => setFormCategory(e.target.value)}
                    className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20"
                    required
                  />
                </div>

                <div>
                  <label className="block font-semibold text-[#1F2A1E] mb-1">Subcategory</label>
                  <input
                    type="text"
                    value={formSubcategory}
                    onChange={(e) => setFormSubcategory(e.target.value)}
                    className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block font-semibold text-[#1F2A1E] mb-1">Base Price (₹)</label>
                  <div className="relative">
                    <span className="absolute left-2.5 top-1/2 -translate-y-1/2 font-bold text-[#1F2A1E]/40 font-mono">₹</span>
                    <input
                      type="number"
                      value={formBasePrice}
                      onChange={(e) => setFormBasePrice(parseFloat(e.target.value) || 0)}
                      className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-6 pr-2 py-2 text-xs font-mono font-bold"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block font-semibold text-[#1F2A1E] mb-1">Max Surge</label>
                  <input
                    type="number"
                    step="0.05"
                    value={formMaxSurge}
                    onChange={(e) => setFormMaxSurge(parseFloat(e.target.value) || 0)}
                    className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-2.5 py-2 text-xs font-mono"
                    required
                  />
                </div>

                <div>
                  <label className="block font-semibold text-[#1F2A1E] mb-1">Max Discount</label>
                  <input
                    type="number"
                    step="0.05"
                    value={formMaxDiscount}
                    onChange={(e) => setFormMaxDiscount(parseFloat(e.target.value) || 0)}
                    className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-2.5 py-2 text-xs font-mono"
                    required
                  />
                </div>
              </div>

              <div className="flex items-center gap-2 pt-2">
                <input
                  type="checkbox"
                  id="createActive"
                  checked={formIsActive}
                  onChange={(e) => setFormIsActive(e.target.checked)}
                  className="rounded text-[#2F5233]"
                />
                <label htmlFor="createActive" className="font-semibold text-[#1F2A1E]">
                  Publish to Catalog Immediately
                </label>
              </div>

              <div className="pt-2 text-[11px] text-[#1F2A1E]/60 italic bg-[#F2EDE1]/60 p-3 rounded-xl border border-[#E5DEC9]">
                ✨ Automatic AI metadata generation will trigger immediately after creation to populate Included/Excluded lists, How It Works steps, and FAQs.
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-[#E5DEC9]">
                <button
                  type="button"
                  onClick={() => setIsCreateOpen(false)}
                  className="px-4 py-2 bg-[#F2EDE1] text-[#1F2A1E] font-semibold rounded-xl text-xs hover:bg-[#E5DEC9] transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createLoading}
                  className="flex items-center gap-2 px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-semibold rounded-xl text-xs shadow-xs disabled:opacity-50 cursor-pointer"
                >
                  {createLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                  <span>Create & Generate AI Content</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Pre-Import Validation & Preview Modal */}
      {previewModalOpen && previewData && (
        <div className="fixed inset-0 z-50 bg-[#1F2A1E]/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-4xl rounded-3xl shadow-2xl border border-[#E5DEC9] overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in">
            {/* Header */}
            <div className="flex items-center justify-between px-8 py-5 border-b border-[#E5DEC9] bg-[#FAF7F0]">
              <div>
                <h3 className="font-bold font-serif text-[#1F2A1E] text-lg flex items-center gap-2">
                  <FileSpreadsheet className="w-5 h-5 text-[#2F5233]" />
                  <span>Excel Catalog Pre-Import Validation & Preview</span>
                </h3>
                <p className="text-xs text-[#1F2A1E]/60 font-semibold mt-0.5">
                  Spreadsheet: <strong className="text-[#1F2A1E]">{importFile?.name}</strong> • {previewData.total_rows} Rows Analyzed
                </p>
              </div>
              <button
                onClick={() => setPreviewModalOpen(false)}
                className="p-1 text-[#1F2A1E]/40 hover:text-[#1F2A1E] rounded-lg cursor-pointer"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Content Body */}
            <div className="p-6 md:p-8 overflow-y-auto space-y-6 text-sm">
              {/* Summary Cards */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-center">
                <div className="p-3 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9]">
                  <span className="text-[10px] uppercase font-bold text-[#1F2A1E]/40">Total Rows</span>
                  <p className="text-xl font-bold font-serif text-[#1F2A1E] mt-1">{previewData.total_rows}</p>
                </div>
                <div className="p-3 bg-emerald-50 rounded-2xl border border-emerald-200">
                  <span className="text-[10px] uppercase font-bold text-emerald-700">Valid Rows</span>
                  <p className="text-xl font-bold font-serif text-emerald-800 mt-1">{previewData.valid_count}</p>
                </div>
                <div className="p-3 bg-[#F2EDE1] rounded-2xl border border-[#E5DEC9]">
                  <span className="text-[10px] uppercase font-bold text-[#2F5233]">Updates (Existing)</span>
                  <p className="text-xl font-bold font-serif text-[#2F5233] mt-1">{previewData.updates_count}</p>
                </div>
                <div className="p-3 bg-[#F2EDE1] rounded-2xl border border-[#E5DEC9]">
                  <span className="text-[10px] uppercase font-bold text-[#C9A15A]">New Services</span>
                  <p className="text-xl font-bold font-serif text-[#1F2A1E] mt-1">{previewData.new_count}</p>
                </div>
                <div className={`p-3 rounded-2xl border ${previewData.invalid_count > 0 ? 'bg-rose-50 border-rose-200 text-rose-800' : 'bg-[#FAF7F0] border-[#E5DEC9] text-[#1F2A1E]/40'}`}>
                  <span className="text-[10px] uppercase font-bold">Invalid Rows</span>
                  <p className="text-xl font-bold font-serif mt-1">{previewData.invalid_count}</p>
                </div>
              </div>

              {/* Error Warnings Box */}
              {previewData.invalid_count > 0 && (
                <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl space-y-2">
                  <div className="flex items-center gap-2 text-rose-800 font-bold text-sm">
                    <AlertCircle className="w-4 h-4 text-rose-600" />
                    <span>Row Validation Errors Detected ({previewData.errors.length})</span>
                  </div>
                  <ul className="list-disc list-inside text-xs text-rose-700 space-y-1 font-medium max-h-32 overflow-y-auto">
                    {previewData.errors.map((err: string, i: number) => (
                      <li key={i}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Rows Preview Table */}
              <div className="space-y-2">
                <h4 className="font-bold text-[#1F2A1E] text-sm font-serif">Spreadsheet Rows Breakdown</h4>
                <div className="border border-[#E5DEC9] rounded-2xl overflow-hidden max-h-60 overflow-y-auto">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-[#F2EDE1] text-[#1F2A1E] font-bold uppercase text-[10px]">
                      <tr>
                        <th className="py-2.5 px-3">Row #</th>
                        <th className="py-2.5 px-3">Service ID</th>
                        <th className="py-2.5 px-3">Category</th>
                        <th className="py-2.5 px-3">Subcategory</th>
                        <th className="py-2.5 px-3">Service Name</th>
                        <th className="py-2.5 px-3">Base Price</th>
                        <th className="py-2.5 px-3">Action</th>
                        <th className="py-2.5 px-3">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E5DEC9]">
                      {previewData.rows_preview?.map((row: any) => (
                        <tr key={row.row_number} className={row.status === 'INVALID' ? 'bg-rose-50/50' : 'hover:bg-[#FAF7F0]'}>
                          <td className="py-2 px-3 font-bold text-[#1F2A1E]">{row.row_number}</td>
                          <td className="py-2 px-3 font-mono text-[#1F2A1E]/60 max-w-[100px] truncate">{row.service_id || '—'}</td>
                          <td className="py-2 px-3 text-[#1F2A1E] font-medium">{row.category}</td>
                          <td className="py-2 px-3 text-[#1F2A1E] font-medium">{row.subcategory}</td>
                          <td className="py-2 px-3 font-bold text-[#1F2A1E]">{row.name}</td>
                          <td className="py-2 px-3 font-mono font-bold text-[#1F2A1E]">{row.base_price}</td>
                          <td className="py-2 px-3 font-bold">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] ${
                              row.action_type === 'UPDATE' ? 'bg-[#F2EDE1] text-[#2F5233]' :
                              row.action_type === 'INSERT' ? 'bg-purple-100 text-purple-800' : 'bg-rose-100 text-rose-800'
                            }`}>
                              {row.action_type}
                            </span>
                          </td>
                          <td className="py-2 px-3 font-bold">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] ${
                              row.status === 'VALID' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                            }`}>
                              {row.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-between px-8 py-4 border-t border-[#E5DEC9] bg-[#FAF7F0]">
              <span className="text-xs text-[#1F2A1E]/60 font-semibold">
                🔒 Database modification is paused until you confirm.
              </span>
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => setPreviewModalOpen(false)}
                  className="px-5 py-2.5 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E] font-bold rounded-2xl text-xs transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleConfirmImport}
                  disabled={confirmImportLoading || previewData.invalid_count > 0 || previewData.valid_count === 0}
                  className="flex items-center gap-2 px-6 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-2xl text-xs shadow-xs transition-colors disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
                >
                  {confirmImportLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                  <span>Confirm & Process Import ({previewData.valid_count} Valid Rows)</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
