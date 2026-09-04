import React, { useEffect, useState, useMemo } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { 
  getCatalogCategories, 
  getCatalogServices, 
  CategoryItem, 
  ServiceItem 
} from '../api/catalog';
import { formatCurrencyINR } from '../utils/formatters';
import { getServiceImage, formatCategoryDisplayName, DEFAULT_SERVICE_IMAGE } from '../utils/serviceImages';
import { 
  Search, 
  Star, 
  Clock, 
  Loader2, 
  AlertCircle,
  RefreshCw,
  Layers,
  ChevronRight,
  FolderTree,
  CheckCircle2,
  LayoutGrid,
  List,
  ArrowLeft,
  Check
} from 'lucide-react';

export const CustomerCatalog: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const activeCategoryParam = searchParams.get('category') || '';
  const activeSubcategoryParam = searchParams.get('subcategory') || '';
  const searchQueryParam = searchParams.get('q') || '';
  const viewAllParam = searchParams.get('view') === 'all';

  const [categories, setCategories] = useState<CategoryItem[]>([]);
  const [allServices, setAllServices] = useState<ServiceItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedCategory, setSelectedCategory] = useState<string>(activeCategoryParam);
  const [selectedSubcategory, setSelectedSubcategory] = useState<string>(activeSubcategoryParam);
  const [searchQuery, setSearchQuery] = useState<string>(searchQueryParam);
  const [viewAllServices, setViewAllServices] = useState<boolean>(viewAllParam);
  const [sortBy, setSortBy] = useState<string>('default');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const fetchCatalog = async () => {
    setLoading(true);
    setError(null);
    try {
      const catRes = await getCatalogCategories();
      setCategories(catRes);
      const srvRes = await getCatalogServices();
      setAllServices(srvRes);
    } catch (err: any) {
      console.error('Catalog fetch error:', err);
      if (err.response) {
        setError(err.response.data?.detail || `API Error (${err.response.status}): Failed to load backend catalog.`);
      } else if (err.request) {
        setError('Unable to connect to SmartServe API. Please verify network connectivity and backend server availability.');
      } else {
        setError(err.message || 'An unexpected error occurred while loading the catalog.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCatalog();
  }, []);

  useEffect(() => {
    setSelectedCategory(searchParams.get('category') || '');
    setSelectedSubcategory(searchParams.get('subcategory') || '');
    setSearchQuery(searchParams.get('q') || '');
    setViewAllServices(searchParams.get('view') === 'all');
  }, [searchParams]);

  // Derived current category object
  const currentCategoryObj = useMemo(() => {
    if (!selectedCategory) return null;
    return categories.find(
      c => c.name.toLowerCase() === selectedCategory.toLowerCase() ||
           (c.display_name && c.display_name.toLowerCase() === selectedCategory.toLowerCase())
    );
  }, [categories, selectedCategory]);

  // Derived available subcategories for selected category
  const currentSubcategories = useMemo(() => {
    if (currentCategoryObj && currentCategoryObj.subcategories && currentCategoryObj.subcategories.length > 0) {
      return currentCategoryObj.subcategories;
    }
    if (!selectedCategory) return [];
    const subsMap = new Map<string, { service_count: number; active_count: number }>();
    allServices
      .filter(s => s.category.toLowerCase() === selectedCategory.toLowerCase())
      .forEach(s => {
        const sub = s.subcategory || 'General';
        if (!subsMap.has(sub)) {
          subsMap.set(sub, { service_count: 0, active_count: 0 });
        }
        const item = subsMap.get(sub)!;
        item.service_count += 1;
        if (s.is_active) item.active_count += 1;
      });
    return Array.from(subsMap.entries()).map(([name, counts]) => ({
      name,
      service_count: counts.service_count,
      active_count: counts.active_count
    })).sort((a, b) => a.name.localeCompare(b.name));
  }, [currentCategoryObj, selectedCategory, allServices]);

  // Filtered Services for Level 3
  const displayedServices = useMemo(() => {
    let result = allServices.filter(s => s.is_active);

    if (selectedCategory) {
      result = result.filter(s => s.category.toLowerCase() === selectedCategory.toLowerCase());
    }

    if (selectedSubcategory) {
      result = result.filter(s => s.subcategory && s.subcategory.toLowerCase() === selectedSubcategory.toLowerCase());
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(s => 
        s.name.toLowerCase().includes(q) ||
        s.category.toLowerCase().includes(q) ||
        (s.subcategory && s.subcategory.toLowerCase().includes(q)) ||
        (s.description && s.description.toLowerCase().includes(q))
      );
    }

    if (sortBy === 'price_asc') {
      result.sort((a, b) => a.base_price - b.base_price);
    } else if (sortBy === 'price_desc') {
      result.sort((a, b) => b.base_price - a.base_price);
    } else if (sortBy === 'name') {
      result.sort((a, b) => a.name.localeCompare(b.name));
    }

    return result;
  }, [allServices, selectedCategory, selectedSubcategory, searchQuery, sortBy]);

  // Navigation handlers
  const handleSelectCategory = (catName: string) => {
    setSelectedCategory(catName);
    setSelectedSubcategory('');
    setViewAllServices(false);
    setSearchParams({ category: catName });
  };

  const handleSelectSubcategory = (subName: string) => {
    setSelectedSubcategory(subName);
    const params: Record<string, string> = {};
    if (selectedCategory) params.category = selectedCategory;
    if (subName) params.subcategory = subName;
    setSearchParams(params);
  };

  const handleResetToCategories = () => {
    setSelectedCategory('');
    setSelectedSubcategory('');
    setSearchQuery('');
    setViewAllServices(false);
    setSearchParams({});
  };

  const handleViewAllClick = () => {
    setSelectedCategory('');
    setSelectedSubcategory('');
    setViewAllServices(true);
    setSearchParams({ view: 'all' });
  };

  // Determine current active level in hierarchy
  const isLevel3 = Boolean(selectedSubcategory || searchQuery.trim() || viewAllServices);
  const isLevel2 = Boolean(selectedCategory && !selectedSubcategory && !searchQuery.trim() && !viewAllServices);
  const isLevel1 = !isLevel2 && !isLevel3;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4 font-sans">
        <Loader2 className="w-10 h-10 animate-spin text-[#2563EB]" />
        <p className="text-base font-semibold text-slate-700">Loading SmartServe Master Catalog...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 bg-white border border-red-200 rounded-3xl shadow-sm text-center space-y-4 font-sans">
        <div className="w-12 h-12 rounded-2xl bg-red-50 text-red-500 mx-auto flex items-center justify-center">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h3 className="text-xl font-bold text-slate-900">Catalog Loading Error</h3>
        <p className="text-sm text-slate-600 max-w-md mx-auto">{error}</p>
        <button
          onClick={fetchCatalog}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] text-white text-xs font-bold rounded-xl shadow-xs"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 font-sans max-w-7xl mx-auto pb-12">

      {/* BREADCRUMB HIERARCHY BAR */}
      <nav className="flex items-center gap-2 text-xs font-bold text-slate-500 flex-wrap">
        <button 
          onClick={handleResetToCategories}
          className={`hover:text-[#2563EB] transition-colors ${isLevel1 ? 'text-[#2563EB]' : ''}`}
        >
          All Categories
        </button>

        {selectedCategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
            <button 
              onClick={() => handleSelectCategory(selectedCategory)}
              className={`hover:text-[#2563EB] transition-colors ${isLevel2 ? 'text-[#2563EB]' : ''}`}
            >
              {formatCategoryDisplayName(selectedCategory)}
            </button>
          </>
        )}

        {selectedSubcategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
            <span className="text-slate-900 font-extrabold">{selectedSubcategory}</span>
          </>
        )}

        {viewAllServices && !selectedCategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
            <span className="text-slate-900 font-extrabold">All Services Catalog</span>
          </>
        )}
      </nav>

      {/* SEARCH & QUICK ACTION BAR */}
      <div className="bg-white p-4 sm:p-5 rounded-3xl border border-slate-200/90 shadow-2xs flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              if (e.target.value.trim()) {
                setSearchParams({ q: e.target.value.trim() });
              } else if (selectedCategory) {
                setSearchParams({ category: selectedCategory });
              } else {
                setSearchParams({});
              }
            }}
            placeholder="Search verified services across all categories (e.g. AC repair, facial, deep cleaning)..."
            className="w-full bg-slate-50 border border-slate-200 rounded-2xl pl-11 pr-4 py-2.5 text-xs font-semibold text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/30"
          />
        </div>

        <div className="flex items-center gap-2 flex-wrap justify-end">
          <button
            onClick={handleViewAllClick}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
              viewAllServices
                ? 'bg-[#2563EB] text-white shadow-xs'
                : 'bg-slate-100 hover:bg-slate-200/80 text-slate-700'
            }`}
          >
            <span>View All ({allServices.length})</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* LEVEL 1 — CATEGORY GRID (When on root catalog) */}
      {/* ========================================================================= */}
      {isLevel1 && (
        <div className="space-y-6 animate-in fade-in duration-200">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Service Categories</h1>
              <span className="text-xs font-bold text-[#2563EB] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
                {categories.length} Categories
              </span>
            </div>
            <p className="text-sm text-slate-500 font-medium mt-1">
              Select a category to view specialized subcategories and verified services.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((cat) => {
              const catImage = getServiceImage(cat.name);
              return (
                <div
                  key={cat.id || cat.name}
                  onClick={() => handleSelectCategory(cat.name)}
                  className="group bg-white rounded-3xl border border-slate-200/90 shadow-2xs hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
                >
                  {/* Category Photography Cover */}
                  <div className="relative w-full h-44 bg-slate-100 overflow-hidden">
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
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-950/75 via-slate-900/25 to-transparent"></div>

                    <div className="absolute bottom-3.5 left-4 right-4 flex items-end justify-between">
                      <div>
                        <h3 className="text-lg font-bold text-white tracking-tight drop-shadow-sm">
                          {cat.display_name || formatCategoryDisplayName(cat.name)}
                        </h3>
                        <p className="text-xs text-slate-200 font-medium mt-0.5">
                          {cat.subcategories_count || (cat.subcategories?.length || 0)} Subcategories • {cat.service_count} Services
                        </p>
                      </div>

                      <div className="w-8 h-8 rounded-full bg-white/20 backdrop-blur-xs text-white flex items-center justify-center group-hover:bg-[#2563EB] transition-colors flex-shrink-0">
                        <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                      </div>
                    </div>
                  </div>

                  {/* Card Bottom Meta */}
                  <div className="p-4 sm:p-5 flex items-center justify-between text-xs">
                    <span className="inline-flex items-center gap-1.5 text-emerald-700 font-bold bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                      <span>{cat.active_count || cat.service_count} Active Services</span>
                    </span>

                    <span className="font-bold text-[#2563EB] group-hover:underline flex items-center gap-1">
                      <span>Explore</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* LEVEL 2 — SUBCATEGORY GRID (When a Category is selected) */}
      {/* ========================================================================= */}
      {isLevel2 && (
        <div className="space-y-6 animate-in fade-in duration-200">
          <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleResetToCategories}
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-slate-800 transition-colors"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Back to Categories</span>
                </button>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mt-2">
                {formatCategoryDisplayName(selectedCategory)}
              </h1>
              <p className="text-sm text-slate-500 font-medium mt-1">
                {currentSubcategories.length} Subcategories • {displayedServices.length} Services available under this category.
              </p>
            </div>

            <button
              onClick={() => handleSelectSubcategory('')}
              className="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-xs flex items-center gap-2 flex-shrink-0"
            >
              <span>View All {formatCategoryDisplayName(selectedCategory)} Services</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {currentSubcategories.map((sub) => {
              const subImage = getServiceImage(selectedCategory, sub.name);
              return (
                <div
                  key={sub.name}
                  onClick={() => handleSelectSubcategory(sub.name)}
                  className="group bg-white rounded-3xl border border-slate-200/90 shadow-2xs hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
                >
                  {/* Subcategory Photography Cover */}
                  <div className="relative w-full h-40 bg-slate-100 overflow-hidden">
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
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-950/75 via-slate-900/25 to-transparent"></div>

                    <div className="absolute bottom-3 left-4 right-4 flex items-end justify-between">
                      <div>
                        <h3 className="text-base sm:text-lg font-bold text-white tracking-tight drop-shadow-sm">
                          {sub.name}
                        </h3>
                        <p className="text-xs text-slate-200 font-medium mt-0.5">
                          {sub.service_count} Services Available
                        </p>
                      </div>

                      <div className="w-8 h-8 rounded-full bg-white/20 backdrop-blur-xs text-white flex items-center justify-center group-hover:bg-[#2563EB] transition-colors flex-shrink-0">
                        <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                      </div>
                    </div>
                  </div>

                  {/* Subcategory Bottom Bar */}
                  <div className="p-4 sm:p-5 flex items-center justify-between text-xs">
                    <span className="inline-flex items-center gap-1.5 text-emerald-700 font-bold bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                      <span>{sub.active_count} Active</span>
                    </span>

                    <span className="font-bold text-[#2563EB] group-hover:underline flex items-center gap-1">
                      <span>Browse Services</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* LEVEL 3 — SERVICE LIST VIEW (When subcategory or search/all is active) */}
      {/* ========================================================================= */}
      {isLevel3 && (
        <div className="space-y-6 animate-in fade-in duration-200">
          {/* Header & Subcategory Switcher */}
          <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-2xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={selectedCategory ? () => handleSelectCategory(selectedCategory) : handleResetToCategories}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-slate-800 transition-colors"
                  >
                    <ArrowLeft className="w-3.5 h-3.5" />
                    <span>Back to {selectedCategory ? formatCategoryDisplayName(selectedCategory) : 'Categories'}</span>
                  </button>
                </div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mt-2">
                  {selectedSubcategory || (selectedCategory ? formatCategoryDisplayName(selectedCategory) : 'Services Catalog')}
                </h1>
                <p className="text-sm text-slate-500 font-medium mt-1">
                  Showing {displayedServices.length} verified services managed live in the database.
                </p>
              </div>

              {/* View mode & Sort controls */}
              <div className="flex items-center gap-3">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-bold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/30"
                >
                  <option value="default">Default Sorting</option>
                  <option value="price_asc">Price: Low to High</option>
                  <option value="price_desc">Price: High to Low</option>
                  <option value="name">Service Name (A-Z)</option>
                </select>

                <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-1.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white text-[#2563EB] shadow-xs' : 'text-slate-500 hover:text-slate-800'}`}
                    title="Grid View"
                  >
                    <LayoutGrid className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-1.5 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-white text-[#2563EB] shadow-xs' : 'text-slate-500 hover:text-slate-800'}`}
                    title="List View"
                  >
                    <List className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Sister Subcategory Quick Switcher Chips */}
            {selectedCategory && currentSubcategories.length > 0 && (
              <div className="flex items-center gap-2 overflow-x-auto pt-3 border-t border-slate-100 scrollbar-none">
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex-shrink-0 mr-1 flex items-center gap-1">
                  <Layers className="w-3 h-3 text-blue-500" />
                  Subcategories:
                </span>
                <button
                  onClick={() => handleSelectSubcategory('')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all flex-shrink-0 ${
                    selectedSubcategory === ''
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  All ({allServices.filter(s => s.category.toLowerCase() === selectedCategory.toLowerCase()).length})
                </button>
                {currentSubcategories.map((sub) => {
                  const isSubActive = selectedSubcategory.toLowerCase() === sub.name.toLowerCase();
                  return (
                    <button
                      key={sub.name}
                      onClick={() => handleSelectSubcategory(sub.name)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all flex-shrink-0 ${
                        isSubActive
                          ? 'bg-[#2563EB] text-white shadow-xs'
                          : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                      }`}
                    >
                      {sub.name} ({sub.service_count})
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Empty State */}
          {displayedServices.length === 0 ? (
            <div className="py-16 text-center bg-white rounded-3xl border border-slate-200 shadow-2xs space-y-3">
              <FolderTree className="w-10 h-10 text-slate-400 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No Services Found</h3>
              <p className="text-xs text-slate-500 font-medium">No services match your active filters or search terms.</p>
              <button
                onClick={handleResetToCategories}
                className="inline-flex items-center gap-2 px-4 py-2 bg-[#2563EB] text-white rounded-xl text-xs font-bold mt-2"
              >
                <span>Clear Filters & View Categories</span>
              </button>
            </div>
          ) : viewMode === 'grid' ? (
            /* Service Cards Grid View */
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {displayedServices.map((svc) => {
                const serviceImg = getServiceImage(svc.category, svc.subcategory, svc.name);
                const hasFeatures = svc.included && svc.included.length > 0;
                const featuresPreview = hasFeatures ? svc.included!.slice(0, 2) : (svc.features || []).slice(0, 2);

                return (
                  <div
                    key={svc.id}
                    onClick={() => navigate(`/service/${svc.id}`)}
                    className="group bg-white rounded-3xl border border-slate-200/90 shadow-2xs hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
                  >
                    {/* Real Service Image Cover */}
                    <div className="relative w-full h-44 bg-slate-100 overflow-hidden">
                      <img
                        src={serviceImg}
                        alt={svc.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        loading="lazy"
                        onError={(e) => {
                          e.currentTarget.onerror = null;
                          e.currentTarget.src = DEFAULT_SERVICE_IMAGE;
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent"></div>

                      {/* Top Badges: Rating & Duration */}
                      <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-xs text-white text-[11px] font-bold">
                          <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                          <span>{svc.rating || 4.8}</span>
                        </span>

                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-xs text-white text-[11px] font-bold">
                          <Clock className="w-3 h-3 text-slate-200" />
                          <span>{svc.duration_minutes || 45} Mins</span>
                        </span>
                      </div>

                      {/* Subcategory badge on image bottom */}
                      <div className="absolute bottom-2.5 left-3">
                        <span className="inline-block px-2.5 py-0.5 rounded-lg bg-black/60 backdrop-blur-xs text-white text-[11px] font-bold">
                          {svc.subcategory}
                        </span>
                      </div>
                    </div>

                    {/* Card Content */}
                    <div className="p-5 flex-1 flex flex-col justify-between space-y-3">
                      <div>
                        <div className="flex items-center gap-1.5 text-[11px] font-bold text-blue-600 uppercase tracking-wider">
                          <span>{formatCategoryDisplayName(svc.category)}</span>
                        </div>
                        <h3 className="text-base sm:text-lg font-bold text-slate-900 group-hover:text-[#2563EB] transition-colors line-clamp-1 mt-0.5">
                          {svc.name}
                        </h3>
                        {svc.description && (
                          <p className="text-xs text-slate-500 font-normal line-clamp-2 mt-1 leading-relaxed">
                            {svc.description}
                          </p>
                        )}
                      </div>

                      {/* Included Feature Highlights Preview */}
                      {featuresPreview.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-slate-100 text-xs text-slate-600 font-medium">
                          {featuresPreview.map((f, i) => (
                            <div key={i} className="flex items-center gap-1.5 truncate">
                              <Check className="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" />
                              <span className="truncate">{f}</span>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Pricing & Booking Footer */}
                      <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-3">
                        <div>
                          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Price</span>
                          <span className="text-xl font-extrabold text-slate-900 font-mono">
                            {formatCurrencyINR(svc.base_price)}
                          </span>
                        </div>

                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/service/${svc.id}`);
                          }}
                          className="px-4 py-2 bg-[#2563EB] hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-xs"
                        >
                          Book Service
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            /* Service List View */
            <div className="space-y-3">
              {displayedServices.map((svc) => {
                const serviceImg = getServiceImage(svc.category, svc.subcategory, svc.name);
                return (
                  <div
                    key={svc.id}
                    onClick={() => navigate(`/service/${svc.id}`)}
                    className="group bg-white p-4 sm:p-5 rounded-2xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-blue-300 transition-all cursor-pointer flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4"
                  >
                    <div className="flex items-center gap-4">
                      <img
                        src={serviceImg}
                        alt={svc.name}
                        className="w-20 h-20 rounded-xl object-cover flex-shrink-0"
                        onError={(e) => {
                          e.currentTarget.onerror = null;
                          e.currentTarget.src = DEFAULT_SERVICE_IMAGE;
                        }}
                      />
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-[#2563EB] bg-blue-50 px-2 py-0.5 rounded-md">
                            {svc.subcategory}
                          </span>
                          <span className="text-xs font-semibold text-slate-400">
                            {formatCategoryDisplayName(svc.category)}
                          </span>
                        </div>
                        <h3 className="text-base font-bold text-slate-900 group-hover:text-[#2563EB] transition-colors">
                          {svc.name}
                        </h3>
                        {svc.description && (
                          <p className="text-xs text-slate-500 font-normal line-clamp-1 max-w-xl">
                            {svc.description}
                          </p>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center justify-between sm:justify-end gap-6 pt-3 sm:pt-0 border-t sm:border-t-0 border-slate-100 flex-shrink-0">
                      <div className="text-left sm:text-right">
                        <span className="text-lg font-extrabold text-slate-900 font-mono block">
                          {formatCurrencyINR(svc.base_price)}
                        </span>
                        <span className="text-xs font-semibold text-slate-500">
                          {svc.duration_minutes || 45} Mins
                        </span>
                      </div>

                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/service/${svc.id}`);
                        }}
                        className="px-4 py-2 bg-[#2563EB] hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-xs"
                      >
                        Book Now
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

    </div>
  );
};

export default CustomerCatalog;
