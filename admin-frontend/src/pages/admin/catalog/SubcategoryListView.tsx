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
  ArrowLeft
} from 'lucide-react';
import { getCatalogServices } from '../../../api/catalog';
import type { ServiceItem } from '../../../api/catalog';
import { getCategoryIcon, getServiceIcon } from '../../../utils/catalogIcons';

export const SubcategoryListView: React.FC = () => {
  const { categoryName } = useParams<{ categoryName: string }>();
  const navigate = useNavigate();
  const decodedCategory = decodeURIComponent(categoryName || '');

  const [services, setServices] = useState<ServiceItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const fetchCategoryServices = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCatalogServices(decodedCategory);
      setServices(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load subcategories.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (decodedCategory) {
      fetchCategoryServices();
    }
  }, [decodedCategory]);

  // Group services by subcategory
  const subcategorySummaries = useMemo(() => {
    const map = new Map<string, { total: number; active: number }>();

    services.forEach((s) => {
      if (!map.has(s.subcategory)) {
        map.set(s.subcategory, { total: 0, active: 0 });
      }
      const item = map.get(s.subcategory)!;
      item.total += 1;
      if (s.is_active) item.active += 1;
    });

    const result: Array<{
      name: string;
      serviceCount: number;
      activeCount: number;
    }> = [];

    map.forEach((val, name) => {
      result.push({
        name,
        serviceCount: val.total,
        activeCount: val.active,
      });
    });

    return result.sort((a, b) => a.name.localeCompare(b.name));
  }, [services]);

  const filteredSubcategories = useMemo(() => {
    return subcategorySummaries.filter((sub) =>
      sub.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [subcategorySummaries, searchTerm]);

  const totalCategoryServices = services.length;
  const activeCategoryServices = services.filter((s) => s.is_active).length;
  const CategoryIcon = getCategoryIcon(decodedCategory);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-medium text-slate-600">Loading subcategories for {decodedCategory}...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-6 bg-white border border-red-200 rounded-2xl shadow-sm text-center space-y-4">
        <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Failed to Load Subcategories</h3>
        <p className="text-xs text-slate-600 max-w-md mx-auto">{error}</p>
        <button
          onClick={fetchCategoryServices}
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
      <nav className="flex items-center gap-2 text-xs text-slate-500 font-medium">
        <Link to="/admin/catalog" className="hover:text-[#5CA8FF] flex items-center gap-1 transition-colors">
          <FolderTree className="w-3.5 h-3.5" />
          <span>Catalog</span>
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <span className="text-slate-900 font-bold">{decodedCategory}</span>
      </nav>

      {/* Level 2 Header Card */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-start gap-4">
          <button
            onClick={() => navigate('/admin/catalog')}
            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors mt-0.5"
            title="Back to Categories"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-blue-50 text-[#5CA8FF]">
                <CategoryIcon className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">{decodedCategory}</h1>
                <p className="text-sm text-slate-500 font-semibold mt-0.5">
                  {subcategorySummaries.length} Subcategories • {totalCategoryServices} Services Total
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 bg-slate-50 border border-slate-200/80 px-4 py-2.5 rounded-xl text-xs">
          <div>
            <span className="text-[10px] text-slate-400 font-semibold uppercase">Category Active Ratio</span>
            <p className="font-bold text-emerald-600">{activeCategoryServices} of {totalCategoryServices} Active</p>
          </div>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 w-full max-w-md">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search subcategories..."
            className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          />
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-1.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
          >
            <LayoutGrid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-1.5 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
          >
            <List className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Subcategory Grid or List Render */}
      {filteredSubcategories.length === 0 ? (
        <div className="py-16 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-3">
          <FolderTree className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-sm font-bold text-slate-800">No Subcategories Found</h3>
          <p className="text-xs text-slate-500">No subcategories match your search query.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredSubcategories.map((sub) => {
            const SubIcon = getServiceIcon(sub.name, decodedCategory);
            return (
              <div
                key={sub.name}
                onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(decodedCategory)}/subcategory/${encodeURIComponent(sub.name)}`)}
                className="group bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-xl bg-blue-50 group-hover:bg-[#5CA8FF] text-[#5CA8FF] group-hover:text-white flex items-center justify-center transition-colors">
                      <SubIcon className="w-5 h-5" />
                    </div>
                    <ChevronRight className="w-5 h-5 text-slate-300 group-hover:text-[#5CA8FF] group-hover:translate-x-1 transition-all" />
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900 group-hover:text-[#5CA8FF] transition-colors">
                      {sub.name}
                    </h3>
                    <p className="text-xs text-slate-500 mt-1">
                      {sub.serviceCount} Services Included
                    </p>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="inline-flex items-center gap-1.5 text-emerald-700 font-semibold bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-100">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                    <span>{sub.activeCount} Active</span>
                  </span>

                  <span className="text-[11px] font-medium text-slate-400 group-hover:text-[#5CA8FF]">
                    View Services →
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="divide-y divide-slate-100">
            {filteredSubcategories.map((sub) => {
              const SubIcon = getServiceIcon(sub.name, decodedCategory);
              return (
                <div
                  key={sub.name}
                  onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(decodedCategory)}/subcategory/${encodeURIComponent(sub.name)}`)}
                  className="p-4 flex items-center justify-between hover:bg-slate-50 transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-9 h-9 rounded-xl bg-blue-50 text-[#5CA8FF] flex items-center justify-center">
                      <SubIcon className="w-4 h-4" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-slate-900">{sub.name}</h3>
                      <p className="text-xs text-slate-500">{sub.serviceCount} Services</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-lg">
                      {sub.activeCount} Active
                    </span>
                    <ChevronRight className="w-4 h-4 text-slate-400" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
