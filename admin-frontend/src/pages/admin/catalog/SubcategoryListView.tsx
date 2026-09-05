import React, { useEffect, useState, useMemo } from 'react';
import { useParams, useSearchParams, useNavigate, Link } from 'react-router-dom';
import { 
  ChevronRight, 
  Search, 
  LayoutGrid, 
  List, 
  RefreshCw, 
  AlertCircle,
  FolderTree,
  CheckCircle2,
  ArrowLeft
} from 'lucide-react';
import { getCatalogServices } from '../../../api/catalog';
import type { ServiceItem } from '../../../api/catalog';
import { getCategoryIcon } from '../../../utils/catalogIcons';
import { getServiceImage, formatCategoryDisplayName, DEFAULT_SERVICE_IMAGE } from '../../../utils/serviceImages';
import { SmartServeLoader } from '../../../components/common/SmartServeLoader';

function safeDecode(val?: string | null): string {
  if (!val) return '';
  try {
    return decodeURIComponent(val);
  } catch {
    return val;
  }
}

export const SubcategoryListView: React.FC = () => {
  const params = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const rawCat = params.categoryName || params['*'] || searchParams.get('category') || '';
  const decodedCategory = safeDecode(rawCat).trim();

  const [services, setServices] = useState<ServiceItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const fetchCategoryServices = async () => {
    setLoading(true);
    setError(null);
    try {
      let data: ServiceItem[] = [];
      try {
        data = await getCatalogServices(decodedCategory || undefined, undefined, 0, 1000);
      } catch (catErr) {
        data = await getCatalogServices(undefined, undefined, 0, 1000);
      }

      // If backend filtered query returned empty, search full catalog with normalized category match
      if (data.length === 0 && decodedCategory) {
        const allData = await getCatalogServices(undefined, undefined, 0, 1000);
        const normCat = decodedCategory.toLowerCase().replace(/[\s\-_/]+/g, ' ').trim();
        data = allData.filter((s) => {
          const sCat = (s.category || '').toLowerCase().replace(/[\s\-_/]+/g, ' ').trim();
          return sCat === normCat || sCat.includes(normCat) || normCat.includes(sCat);
        });
      }

      setServices(data);
    } catch (err: any) {
      console.error('Failed to load subcategories:', err);
      setError(err.response?.data?.detail || 'Failed to load subcategories.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (decodedCategory) {
      fetchCategoryServices();
    } else {
      setLoading(false);
    }
  }, [decodedCategory]);

  // Group services by subcategory
  const subcategorySummaries = useMemo(() => {
    const map = new Map<string, { total: number; active: number }>();

    services.forEach((s) => {
      const sub = s.subcategory || 'General';
      if (!map.has(sub)) {
        map.set(sub, { total: 0, active: 0 });
      }
      const item = map.get(sub)!;
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
  const displayCategoryName = formatCategoryDisplayName(decodedCategory);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <SmartServeLoader size="lg" text={`Loading subcategories for ${displayCategoryName}...`} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 bg-white border border-red-200 rounded-3xl shadow-sm text-center space-y-4 font-sans">
        <div className="w-12 h-12 rounded-2xl bg-red-50 text-red-500 mx-auto flex items-center justify-center">
          <AlertCircle className="w-6 h-6" />
        </div>
        <div className="space-y-1">
          <h3 className="text-xl font-bold text-slate-900">Failed to Load Subcategories</h3>
          <p className="text-sm text-slate-600 max-w-md mx-auto">{error}</p>
        </div>
        <button
          onClick={fetchCategoryServices}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white rounded-xl text-xs font-bold shadow-xs transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-[#1F2A1E]">
      {/* Clickable Breadcrumbs Navigation */}
      <nav className="flex items-center gap-2 text-xs text-[#1F2A1E]/60 font-semibold overflow-x-auto">
        <Link to="/admin/catalog" className="hover:text-[#2F5233] flex items-center gap-1 transition-colors">
          <FolderTree className="w-3.5 h-3.5 text-[#C9A15A]" />
          <span>Catalog</span>
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-[#E5DEC9] flex-shrink-0" />
        <span className="text-[#1F2A1E] font-bold flex-shrink-0">{displayCategoryName}</span>
      </nav>

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-xs">
        <div className="flex items-start gap-4">
          <button
            onClick={() => navigate('/admin/catalog')}
            className="p-2.5 rounded-xl bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E] transition-colors mt-0.5 cursor-pointer"
            title="Back to Categories"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div className="w-12 h-12 rounded-2xl bg-[#F2EDE1] text-[#2F5233] flex items-center justify-center flex-shrink-0 border border-[#E5DEC9]">
            <CategoryIcon className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-serif text-[#1F2A1E] tracking-tight">{displayCategoryName}</h1>
            <p className="text-xs sm:text-sm text-[#1F2A1E]/60 font-medium mt-0.5">
              {subcategorySummaries.length} Subcategories • {totalCategoryServices} Services Total • {activeCategoryServices} Active
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(decodedCategory)}/subcategory/all`)}
            className="px-4 py-2.5 bg-[#F2EDE1] hover:bg-[#2F5233] hover:text-white text-[#2F5233] font-bold text-xs rounded-xl transition-colors border border-[#E5DEC9] cursor-pointer shadow-2xs"
          >
            View All Services ({totalCategoryServices})
          </button>
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
            placeholder="Search subcategories..."
            className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          />
        </div>

        {/* View Mode Toggle */}
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

      {/* Subcategory Grid or List Render */}
      {filteredSubcategories.length === 0 ? (
        <div className="py-16 text-center bg-white rounded-3xl border border-[#E5DEC9] shadow-xs space-y-3">
          <FolderTree className="w-10 h-10 text-[#1F2A1E]/40 mx-auto" />
          <h3 className="text-base font-bold text-[#1F2A1E]">No Subcategories Found</h3>
          <p className="text-xs text-[#1F2A1E]/60 font-medium">No subcategories match your search query.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredSubcategories.map((sub) => {
            const subImage = getServiceImage(decodedCategory, sub.name);
            return (
              <div
                key={sub.name}
                onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(decodedCategory)}/subcategory/${encodeURIComponent(sub.name)}`)}
                className="group bg-white rounded-3xl border border-[#E5DEC9] shadow-xs hover:shadow-md hover:border-[#2F5233]/40 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
              >
                {/* Subcategory Photography Cover */}
                <div className="relative w-full h-40 bg-[#F2EDE1] overflow-hidden">
                  <img
                    src={subImage}
                    alt={sub.name}
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
                      <h3 className="text-base sm:text-lg font-serif font-bold text-white tracking-tight drop-shadow-xs">
                        {sub.name}
                      </h3>
                      <p className="text-xs text-[#FAF7F0]/90 font-medium">
                        {sub.serviceCount} Services Available
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
                    <span>{sub.activeCount} Active</span>
                  </span>

                  <span className="font-bold text-[#2F5233] group-hover:underline flex items-center gap-1">
                    <span>View Services</span>
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
            {filteredSubcategories.map((sub) => {
              return (
                <div
                  key={sub.name}
                  onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(decodedCategory)}/subcategory/${encodeURIComponent(sub.name)}`)}
                  className="p-4 flex items-center justify-between hover:bg-[#FAF7F0] transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-xl bg-[#F2EDE1] text-[#2F5233] flex items-center justify-center flex-shrink-0 border border-[#E5DEC9]">
                      <FolderTree className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-bold text-[#1F2A1E] text-sm font-serif">{sub.name}</h4>
                      <p className="text-xs text-[#1F2A1E]/60 font-medium">{sub.serviceCount} Services in this subcategory</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                      {sub.activeCount} Active
                    </span>
                    <ChevronRight className="w-4 h-4 text-[#1F2A1E]/40" />
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

export default SubcategoryListView;
