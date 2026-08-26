import React, { useEffect, useState, useMemo } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ChevronRight, 
  Search, 
  LayoutGrid, 
  List, 
  Loader2, 
  RefreshCw, 
  AlertCircle,
  FolderTree,
  CheckCircle2,
  XCircle,
  Sparkles,
  Edit3,
  ChevronLeft,
  ArrowLeft,
  FileSpreadsheet
} from 'lucide-react';
import { getCatalogServices, updateCatalogService, bulkUpdateServiceStatus, exportCatalogExcel } from '../../../api/catalog';
import type { ServiceItem } from '../../../api/catalog';
import { getServiceIcon } from '../../../utils/catalogIcons';
import { formatRupee } from '../../../utils/formatters';

export const ServiceListView: React.FC = () => {
  const { categoryName, subcategoryName } = useParams<{ categoryName: string; subcategoryName: string }>();
  const navigate = useNavigate();
  const decodedCategory = decodeURIComponent(categoryName || '');
  const decodedSubcategory = decodeURIComponent(subcategoryName || '');

  const [services, setServices] = useState<ServiceItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('name_asc');
  const [pageSize, setPageSize] = useState<number>(12);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [currentPage, setCurrentPage] = useState<number>(1);

  // Bulk Selection State
  const [selectedServiceIds, setSelectedServiceIds] = useState<string[]>([]);
  const [bulkConfirmAction, setBulkConfirmAction] = useState<boolean | null>(null);
  const [bulkLoading, setBulkLoading] = useState<boolean>(false);
  const [exportLoading, setExportLoading] = useState<boolean>(false);

  const handleBulkStatusExecute = async (isActive: boolean) => {
    if (selectedServiceIds.length === 0) return;
    setBulkLoading(true);
    try {
      await bulkUpdateServiceStatus(selectedServiceIds, isActive);
      setServices((prev) =>
        prev.map((s) => (selectedServiceIds.includes(s.id) ? { ...s, is_active: isActive } : s))
      );
      setSelectedServiceIds([]);
      setBulkConfirmAction(null);
    } catch (err: any) {
      alert('Failed to perform bulk status update.');
    } finally {
      setBulkLoading(false);
    }
  };

  const handleExportFilteredExcel = async () => {
    setExportLoading(true);
    try {
      await exportCatalogExcel(decodedCategory, decodedSubcategory, searchTerm);
    } catch (err) {
      alert('Failed to export filtered catalog.');
    } finally {
      setExportLoading(false);
    }
  };

  const fetchSubcategoryServices = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCatalogServices(decodedCategory);
      // Filter down to matching subcategory
      const subServices = data.filter((s) => s.subcategory === decodedSubcategory);
      setServices(subServices);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load subcategory services.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (decodedCategory && decodedSubcategory) {
      fetchSubcategoryServices();
    }
  }, [decodedCategory, decodedSubcategory]);

  const filteredServices = useMemo(() => {
    let result = services.filter((s) => {
      const matchesSearch = s.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = !statusFilter || 
        (statusFilter === 'active' && s.is_active) || 
        (statusFilter === 'inactive' && !s.is_active);
      return matchesSearch && matchesStatus;
    });

    result.sort((a, b) => {
      if (sortBy === 'name_asc') return a.name.localeCompare(b.name);
      if (sortBy === 'name_desc') return b.name.localeCompare(a.name);
      if (sortBy === 'price_asc') return a.base_price - b.base_price;
      if (sortBy === 'price_desc') return b.base_price - a.base_price;
      return 0;
    });

    return result;
  }, [services, searchTerm, statusFilter, sortBy]);

  // Reset page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, statusFilter, sortBy, pageSize]);

  // Pagination logic
  const totalItems = filteredServices.length;
  const totalPages = Math.ceil(totalItems / pageSize) || 1;
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, totalItems);
  const paginatedServices = filteredServices.slice(startIndex, endIndex);

  const handleToggleStatus = async (svc: ServiceItem, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const updated = await updateCatalogService(svc.id, { is_active: !svc.is_active });
      setServices((prev) => prev.map((s) => (s.id === updated.id ? updated : s)));
    } catch (err: any) {
      alert('Failed to update service status.');
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-medium text-slate-600">Loading services for {decodedSubcategory}...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-6 bg-white border border-red-200 rounded-2xl shadow-sm text-center space-y-4">
        <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Failed to Load Services</h3>
        <p className="text-xs text-slate-600 max-w-md mx-auto">{error}</p>
        <button
          onClick={fetchSubcategoryServices}
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#5CA8FF] text-white rounded-xl text-xs font-semibold"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Clickable Breadcrumbs Navigation */}
      <nav className="flex items-center gap-2 text-xs text-slate-500 font-medium overflow-x-auto">
        <Link to="/admin/catalog" className="hover:text-[#5CA8FF] flex items-center gap-1 transition-colors">
          <FolderTree className="w-3.5 h-3.5" />
          <span>Catalog</span>
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300 flex-shrink-0" />
        <Link to={`/admin/catalog/category/${encodeURIComponent(decodedCategory)}`} className="hover:text-[#5CA8FF] transition-colors flex-shrink-0">
          {decodedCategory}
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300 flex-shrink-0" />
        <span className="text-slate-900 font-bold flex-shrink-0">{decodedSubcategory}</span>
      </nav>

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-start gap-4">
          <button
            onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(decodedCategory)}`)}
            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors mt-0.5"
            title="Back to Subcategories"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">{decodedSubcategory} Services</h1>
            <p className="text-xs text-slate-500 font-medium mt-0.5">
              Category: <span className="font-semibold text-slate-700">{decodedCategory}</span> • {totalItems} Services Total
            </p>
          </div>
        </div>

        {/* Pagination Info Badge */}
        {totalItems > 0 && (
          <div className="text-xs font-semibold text-slate-600 bg-slate-50 px-3.5 py-2 rounded-xl border border-slate-200/80">
            Showing {startIndex + 1}–{endIndex} of {totalItems} Services
          </div>
        )}
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 w-full max-w-md">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search service name..."
            className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-end">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value="">All Statuses</option>
            <option value="active">Active Only</option>
            <option value="inactive">Inactive Only</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value="name_asc">Sort: Name (A–Z)</option>
            <option value="name_desc">Sort: Name (Z–A)</option>
            <option value="price_asc">Sort: Price (Low → High)</option>
            <option value="price_desc">Sort: Price (High → Low)</option>
          </select>

          <select
            value={pageSize}
            onChange={(e) => setPageSize(Number(e.target.value))}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value={12}>12 / page</option>
            <option value={24}>24 / page</option>
            <option value={48}>48 / page</option>
          </select>

          <button
            onClick={handleExportFilteredExcel}
            disabled={exportLoading}
            className="flex items-center gap-1.5 px-3 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 font-semibold text-xs rounded-xl border border-emerald-200 transition-colors disabled:opacity-50"
            title="Export filtered catalog to Excel"
          >
            {exportLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <FileSpreadsheet className="w-3.5 h-3.5" />}
            <span>Export</span>
          </button>

          {/* Grid / List View Toggle */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="List View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Services Grid or List Render */}
      {paginatedServices.length === 0 ? (
        <div className="py-12 p-6 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <FolderTree className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No services found.</h3>
          <p className="text-sm text-slate-500 font-medium">Try changing your search or filters.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {paginatedServices.map((svc) => {
            const ServiceIcon = getServiceIcon(svc.name, svc.category);
            return (
              <div
                key={svc.id}
                onClick={() => navigate(`/admin/catalog/service/${svc.id}`)}
                className="group bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={selectedServiceIds.includes(svc.id)}
                        onChange={(e) => {
                          e.stopPropagation();
                          if (e.target.checked) {
                            setSelectedServiceIds((prev) => [...prev, svc.id]);
                          } else {
                            setSelectedServiceIds((prev) => prev.filter((id) => id !== svc.id));
                          }
                        }}
                        onClick={(e) => e.stopPropagation()}
                        className="w-4 h-4 rounded text-[#5CA8FF] focus:ring-[#5CA8FF] cursor-pointer"
                      />
                      <div className="w-10 h-10 rounded-xl bg-blue-50 group-hover:bg-[#5CA8FF] text-[#5CA8FF] group-hover:text-white flex items-center justify-center transition-colors">
                        <ServiceIcon className="w-5 h-5" />
                      </div>
                    </div>
                    <button
                      onClick={(e) => handleToggleStatus(svc, e)}
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold transition-colors ${
                        svc.is_active
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-slate-100 text-slate-500 border border-slate-200'
                      }`}
                    >
                      {svc.is_active ? <CheckCircle2 className="w-3 h-3 text-emerald-500" /> : <XCircle className="w-3 h-3 text-slate-400" />}
                      <span>{svc.is_active ? 'Active' : 'Disabled'}</span>
                    </button>
                  </div>

                  <div>
                    <h3 className="text-base md:text-lg font-bold text-slate-900 group-hover:text-[#5CA8FF] transition-colors line-clamp-2">
                      {svc.name}
                    </h3>
                    <p className="text-xs text-slate-500 font-semibold mt-1">
                      {svc.category} • {svc.subcategory}
                    </p>
                  </div>
                </div>

                <div className="mt-5 pt-3 border-t border-slate-100 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-medium text-slate-400 uppercase">Base Price</span>
                    <span className="text-base font-bold text-slate-900 font-mono">
                      {formatRupee(svc.base_price)}
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 bg-slate-50 p-2 rounded-lg border border-slate-100">
                    <span className="text-amber-700">+{(svc.max_demand_increase * 100).toFixed(0)}% Surge</span>
                    <span className="text-emerald-700">-{(svc.max_discount * 100).toFixed(0)}% Discount</span>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-[#5CA8FF] bg-blue-50 px-2 py-0.5 rounded">
                      <Sparkles className="w-3 h-3" />
                      AI Ready
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/admin/catalog/service/${svc.id}`);
                      }}
                      className="inline-flex items-center gap-1 text-xs font-semibold text-slate-700 hover:text-[#5CA8FF]"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                      <span>Manage</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* List View */
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
                  <th className="py-3.5 px-4">Service</th>
                  <th className="py-3.5 px-4">Base Price (INR)</th>
                  <th className="py-3.5 px-4">Max Surge</th>
                  <th className="py-3.5 px-4">Max Discount</th>
                  <th className="py-3.5 px-4">Status</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {paginatedServices.map((svc) => {
                  const ServiceIcon = getServiceIcon(svc.name, svc.category);
                  return (
                    <tr
                      key={svc.id}
                      onClick={() => navigate(`/admin/catalog/service/${svc.id}`)}
                      className="hover:bg-slate-50 transition-colors cursor-pointer"
                    >
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-3">
                          <input
                            type="checkbox"
                            checked={selectedServiceIds.includes(svc.id)}
                            onChange={(e) => {
                              e.stopPropagation();
                              if (e.target.checked) {
                                setSelectedServiceIds((prev) => [...prev, svc.id]);
                              } else {
                                setSelectedServiceIds((prev) => prev.filter((id) => id !== svc.id));
                              }
                            }}
                            onClick={(e) => e.stopPropagation()}
                            className="w-4 h-4 rounded text-[#5CA8FF] focus:ring-[#5CA8FF] cursor-pointer"
                          />
                          <div className="w-8 h-8 rounded-lg bg-blue-50 text-[#5CA8FF] flex items-center justify-center flex-shrink-0">
                            <ServiceIcon className="w-4 h-4" />
                          </div>
                          <div>
                            <p className="font-bold text-slate-900">{svc.name}</p>
                            <p className="text-[11px] text-slate-500">{svc.category} • {svc.subcategory}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-3 px-4 font-mono font-bold text-slate-900 text-sm">
                        {formatRupee(svc.base_price)}
                      </td>
                      <td className="py-3 px-4 font-mono text-amber-700">
                        +{(svc.max_demand_increase * 100).toFixed(0)}%
                      </td>
                      <td className="py-3 px-4 font-mono text-emerald-700">
                        -{(svc.max_discount * 100).toFixed(0)}%
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold ${svc.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'}`}>
                          {svc.is_active ? 'Active' : 'Disabled'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/admin/catalog/service/${svc.id}`);
                          }}
                          className="px-3 py-1 bg-slate-100 hover:bg-[#5CA8FF] hover:text-white text-slate-700 font-semibold rounded-lg transition-colors text-xs"
                        >
                          Manage Service
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Floating Bulk Action Bar */}
      {selectedServiceIds.length > 0 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 bg-slate-900 text-white px-6 py-3.5 rounded-2xl shadow-2xl border border-slate-700 flex items-center gap-4 animate-in slide-in-from-bottom">
          <span className="text-xs font-bold text-slate-300">
            <strong className="text-white text-sm">{selectedServiceIds.length}</strong> Services Selected
          </span>

          <div className="h-4 w-px bg-slate-700" />

          <button
            onClick={() => setBulkConfirmAction(true)}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-xs shadow-xs transition-colors"
          >
            Activate Selected
          </button>

          <button
            onClick={() => setBulkConfirmAction(false)}
            className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl text-xs shadow-xs transition-colors"
          >
            Deactivate Selected
          </button>

          <button
            onClick={() => setSelectedServiceIds([])}
            className="text-xs text-slate-400 hover:text-white underline ml-2"
          >
            Deselect All
          </button>
        </div>
      )}

      {/* Confirmation Modal for Bulk Status Action */}
      {bulkConfirmAction !== null && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-slate-200 p-6 space-y-4 text-center animate-in fade-in">
            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mx-auto ${bulkConfirmAction ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'}`}>
              <AlertCircle className="w-6 h-6" />
            </div>
            <div className="space-y-2">
              <h3 className="text-lg font-bold text-slate-900">
                {bulkConfirmAction ? 'Activate' : 'Deactivate'} {selectedServiceIds.length} Selected Services?
              </h3>
              <p className="text-xs text-slate-600 font-medium">
                {bulkConfirmAction
                  ? 'Selected services will become available for customer bookings immediately.'
                  : 'Selected services will no longer be available for customer bookings. Existing bookings will not be deleted.'}
              </p>
            </div>
            <div className="flex items-center justify-end gap-3 pt-3">
              <button
                onClick={() => setBulkConfirmAction(null)}
                className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl text-xs transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => handleBulkStatusExecute(bulkConfirmAction)}
                disabled={bulkLoading}
                className={`px-5 py-2.5 text-white font-bold rounded-xl text-xs shadow-sm transition-colors ${
                  bulkConfirmAction ? 'bg-emerald-600 hover:bg-emerald-700' : 'bg-rose-600 hover:bg-rose-700'
                }`}
              >
                {bulkLoading ? <Loader2 className="w-4 h-4 animate-spin mx-auto" /> : `Confirm ${bulkConfirmAction ? 'Activation' : 'Deactivation'}`}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Pagination Bar */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between bg-white p-4 rounded-2xl border border-slate-200 shadow-sm text-xs">
          <span className="text-slate-500 font-medium">
            Showing <strong className="text-slate-900">{startIndex + 1}</strong> to <strong className="text-slate-900">{endIndex}</strong> of <strong className="text-slate-900">{totalItems}</strong> services
          </span>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
              disabled={currentPage === 1}
              className="p-2 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-600 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-semibold text-slate-700 px-2">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="p-2 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-600 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
