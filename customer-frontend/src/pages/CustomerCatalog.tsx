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
import { SmartServeLoader } from '../components/common/SmartServeLoader';

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
  const [servicesLoading, setServicesLoading] = useState<boolean>(false);

  // 1. Initial Categories Load
  const fetchCategories = async () => {
    setLoading(true);
    setError(null);
    try {
      const catRes = await getCatalogCategories();
      setCategories(catRes);
    } catch (err: any) {
      console.error('Catalog categories fetch error:', err);
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
    fetchCategories();
  }, []);

  // Sync URL search params to local states
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

  // Derived available subcategories for selected category from live backend category response
  const currentSubcategories = useMemo(() => {
    if (currentCategoryObj && currentCategoryObj.subcategories && currentCategoryObj.subcategories.length > 0) {
      return currentCategoryObj.subcategories;
    }
    return [];
  }, [currentCategoryObj]);

  // 2. Exact Services Load based on active Category / Subcategory / Query
  useEffect(() => {
    const fetchTargetServices = async () => {
      setServicesLoading(true);
      try {
        const params: { category?: string; subcategory?: string; q?: string } = {};
        if (selectedCategory) {
          params.category = currentCategoryObj ? currentCategoryObj.name : selectedCategory;
        }
        if (selectedSubcategory) {
          params.subcategory = selectedSubcategory;
        }
        if (searchQuery.trim()) {
          params.q = searchQuery.trim();
        }
        const srvRes = await getCatalogServices(params);
        setAllServices(srvRes);
      } catch (err: any) {
        console.error('Catalog services fetch error:', err);
      } finally {
        setServicesLoading(false);
      }
    };

    fetchTargetServices();
  }, [selectedCategory, selectedSubcategory, searchQuery, currentCategoryObj]);

  // Filtered & Sorted Services for Level 3
  const displayedServices = useMemo(() => {
    let result = allServices.filter(s => s.is_active);

    const canonicalCat = currentCategoryObj ? currentCategoryObj.name.toLowerCase() : (selectedCategory ? selectedCategory.toLowerCase() : '');

    if (selectedCategory) {
      result = result.filter(
        s => s.category.toLowerCase() === canonicalCat ||
             s.category.toLowerCase().includes(selectedCategory.toLowerCase())
      );
    }

    if (selectedSubcategory) {
      result = result.filter(
        s => s.subcategory && s.subcategory.trim().toLowerCase() === selectedSubcategory.trim().toLowerCase()
      );
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        s => s.name.toLowerCase().includes(q) ||
             s.category.toLowerCase().includes(q) ||
             (s.subcategory && s.subcategory.toLowerCase().includes(q)) ||
             (s.description && s.description.toLowerCase().includes(q))
      );
    }

    // Sort
    if (sortBy === 'price_asc') {
      result.sort((a, b) => a.base_price - b.base_price);
    } else if (sortBy === 'price_desc') {
      result.sort((a, b) => b.base_price - a.base_price);
    } else if (sortBy === 'name') {
      result.sort((a, b) => a.name.localeCompare(b.name));
    }

    return result;
  }, [allServices, selectedCategory, selectedSubcategory, searchQuery, sortBy, currentCategoryObj]);

  // State Level Detection
  const isSearching = searchQuery.trim().length > 0;
  const isLevel1 = !selectedCategory && !selectedSubcategory && !viewAllServices && !isSearching;
  const isLevel2 = selectedCategory !== '' && selectedSubcategory === '' && !viewAllServices && !isSearching;
  const isLevel3 = selectedSubcategory !== '' || viewAllServices || isSearching;

  // Handlers
  const handleSelectCategory = (catName: string) => {
    setSelectedCategory(catName);
    setSelectedSubcategory('');
    setViewAllServices(false);
    setSearchParams({ category: catName });
  };

  const handleSelectSubcategory = (subName: string) => {
    setSelectedSubcategory(subName);
    setViewAllServices(false);
    if (selectedCategory) {
      if (subName) {
        setSearchParams({ category: selectedCategory, subcategory: subName });
      } else {
        setSearchParams({ category: selectedCategory });
      }
    } else {
      if (subName) {
        setSearchParams({ subcategory: subName });
      } else {
        setSearchParams({});
      }
    }
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
    setSearchQuery('');
    setViewAllServices(true);
    setSearchParams({ view: 'all' });
  };

  if (loading && categories.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <SmartServeLoader size="lg" text="Loading SmartServe master catalog..." />
      </div>
    );
  }

  if (error && categories.length === 0) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-[#E5DEC9] rounded-3xl text-center space-y-4 shadow-sm font-sans">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="font-serif text-2xl font-normal text-[#1F2A1E]">Catalog Loading Error</h3>
        <p className="text-sm text-[#1F2A1E]/70 max-w-md mx-auto">{error}</p>
        <button
          onClick={fetchCategories}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white text-xs font-bold rounded-xl shadow-xs transition-colors cursor-pointer"
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
      <nav className="flex items-center gap-2 text-xs font-bold text-[#1F2A1E]/50 flex-wrap">
        <button 
          onClick={handleResetToCategories}
          className={`hover:text-[#2F5233] transition-colors cursor-pointer ${isLevel1 ? 'text-[#2F5233]' : ''}`}
        >
          All Categories
        </button>

        {selectedCategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-[#C9A15A] flex-shrink-0" />
            <button 
              onClick={() => handleSelectCategory(selectedCategory)}
              className={`hover:text-[#2F5233] transition-colors cursor-pointer ${isLevel2 ? 'text-[#2F5233]' : ''}`}
            >
              {formatCategoryDisplayName(selectedCategory)}
            </button>
          </>
        )}

        {selectedSubcategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-[#C9A15A] flex-shrink-0" />
            <span className="text-[#1F2A1E] font-extrabold">{selectedSubcategory}</span>
          </>
        )}

        {viewAllServices && !selectedCategory && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-[#C9A15A] flex-shrink-0" />
            <span className="text-[#1F2A1E] font-extrabold">All Services Catalog</span>
          </>
        )}
      </nav>

      {/* SEARCH & QUICK ACTION BAR */}
      <div className="bg-white p-4 sm:p-5 rounded-3xl border border-[#E5DEC9] shadow-2xs flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-[#1F2A1E]/40 absolute left-4 top-1/2 -translate-y-1/2" />
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
            className="w-full bg-[#F2EDE1]/50 border border-[#E5DEC9] rounded-2xl pl-11 pr-4 py-2.5 text-xs font-semibold text-[#1F2A1E] placeholder:text-[#1F2A1E]/40 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          />
        </div>

        <div className="flex items-center gap-2 flex-wrap justify-end">
          <button
            onClick={handleViewAllClick}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
              viewAllServices
                ? 'bg-[#2F5233] text-white shadow-xs'
                : 'bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E]'
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
              <h1 className="font-serif text-2xl sm:text-3xl font-normal text-[#1F2A1E] tracking-tight">Service Categories</h1>
              <span className="text-xs font-bold text-[#2F5233] bg-[#2F5233]/10 px-3 py-1 rounded-full border border-[#2F5233]/20">
                {categories.length} Primary Categories
              </span>
            </div>
            <p className="text-sm text-[#1F2A1E]/60 font-medium mt-1">
              Select a category to view verified subcategories and bookable services.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((cat) => {
              const catImage = getServiceImage(cat.name);
              return (
                <div
                  key={cat.id || cat.name}
                  onClick={() => handleSelectCategory(cat.name)}
                  className="group bg-white rounded-3xl border border-[#E5DEC9] shadow-2xs hover:shadow-lg hover:border-[#2F5233]/40 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
                >
                  {/* Category Photography Cover */}
                  <div className="relative w-full h-44 bg-[#F2EDE1] overflow-hidden">
                    <img
                      src={catImage}
                      alt={cat.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                      onError={(e) => {
                        e.currentTarget.onerror = null;
                        e.currentTarget.src = DEFAULT_SERVICE_IMAGE;
                      }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#1F2A1E]/85 via-[#1F2A1E]/30 to-transparent" />

                    <div className="absolute bottom-3.5 left-4 right-4 flex items-end justify-between">
                      <div>
                        <h3 className="font-bold text-white text-lg tracking-tight drop-shadow-sm">
                          {cat.display_name || formatCategoryDisplayName(cat.name)}
                        </h3>
                        <p className="text-xs text-[#FAF7F0]/80 font-medium mt-0.5">
                          {cat.subcategories_count || (cat.subcategories?.length || 0)} Subcategories • {cat.service_count} Services
                        </p>
                      </div>

                      <div className="w-8 h-8 rounded-full bg-white/20 backdrop-blur-xs text-white flex items-center justify-center group-hover:bg-[#2F5233] transition-colors flex-shrink-0">
                        <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                      </div>
                    </div>
                  </div>

                  {/* Card Bottom Meta */}
                  <div className="p-4 sm:p-5 flex items-center justify-between text-xs">
                    <span className="inline-flex items-center gap-1.5 text-emerald-800 font-bold bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      <span>{cat.active_count || cat.service_count} Active Services</span>
                    </span>

                    <span className="font-bold text-[#2F5233] group-hover:underline flex items-center gap-1">
                      <span>Explore</span>
                      <ChevronRight className="w-3.5 h-3.5 text-[#C9A15A]" />
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
          <div className="bg-white p-6 sm:p-8 rounded-3xl border border-[#E5DEC9] shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleResetToCategories}
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-[#1F2A1E]/60 hover:text-[#1F2A1E] transition-colors cursor-pointer"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Back to Categories</span>
                </button>
              </div>
              <h1 className="font-serif text-2xl sm:text-3xl font-normal text-[#1F2A1E] tracking-tight mt-2">
                {formatCategoryDisplayName(selectedCategory)}
              </h1>
              <p className="text-sm text-[#1F2A1E]/60 font-medium mt-1">
                {currentSubcategories.length} Subcategories • {displayedServices.length} Services available under this category.
              </p>
            </div>

            <button
              onClick={() => handleSelectSubcategory('')}
              className="px-4 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white rounded-xl text-xs font-bold transition-all shadow-xs flex items-center gap-2 flex-shrink-0 cursor-pointer"
            >
              <span>View All {formatCategoryDisplayName(selectedCategory)} Services</span>
              <ChevronRight className="w-4 h-4 text-[#C9A15A]" />
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {currentSubcategories.map((sub) => {
              const subImage = getServiceImage(selectedCategory, sub.name);
              return (
                <div
                  key={sub.name}
                  onClick={() => handleSelectSubcategory(sub.name)}
                  className="group bg-white rounded-3xl border border-[#E5DEC9] shadow-2xs hover:shadow-lg hover:border-[#2F5233]/40 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
                >
                  {/* Subcategory Photography Cover */}
                  <div className="relative w-full h-40 bg-[#F2EDE1] overflow-hidden">
                    <img
                      src={subImage}
                      alt={sub.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                      onError={(e) => {
                        e.currentTarget.onerror = null;
                        e.currentTarget.src = DEFAULT_SERVICE_IMAGE;
                      }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#1F2A1E]/85 via-[#1F2A1E]/30 to-transparent" />

                    <div className="absolute bottom-3 left-4 right-4 flex items-end justify-between">
                      <div>
                        <h3 className="font-bold text-white text-base sm:text-lg tracking-tight drop-shadow-sm">
                          {sub.name}
                        </h3>
                        <p className="text-xs text-[#FAF7F0]/80 font-medium mt-0.5">
                          {sub.service_count} Services Available
                        </p>
                      </div>

                      <div className="w-8 h-8 rounded-full bg-white/20 backdrop-blur-xs text-white flex items-center justify-center group-hover:bg-[#2F5233] transition-colors flex-shrink-0">
                        <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                      </div>
                    </div>
                  </div>

                  {/* Subcategory Bottom Bar */}
                  <div className="p-4 sm:p-5 flex items-center justify-between text-xs">
                    <span className="inline-flex items-center gap-1.5 text-emerald-800 font-bold bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      <span>{sub.active_count} Active</span>
                    </span>

                    <span className="font-bold text-[#2F5233] group-hover:underline flex items-center gap-1">
                      <span>Browse Services</span>
                      <ChevronRight className="w-3.5 h-3.5 text-[#C9A15A]" />
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
          <div className="bg-white p-6 sm:p-8 rounded-3xl border border-[#E5DEC9] shadow-2xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={selectedCategory ? () => handleSelectCategory(selectedCategory) : handleResetToCategories}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-[#1F2A1E]/60 hover:text-[#1F2A1E] transition-colors cursor-pointer"
                  >
                    <ArrowLeft className="w-3.5 h-3.5" />
                    <span>Back to {selectedCategory ? formatCategoryDisplayName(selectedCategory) : 'Categories'}</span>
                  </button>
                </div>
                <h1 className="font-serif text-2xl sm:text-3xl font-normal text-[#1F2A1E] tracking-tight mt-2">
                  {selectedSubcategory || (selectedCategory ? formatCategoryDisplayName(selectedCategory) : 'Services Catalog')}
                </h1>
                <p className="text-sm text-[#1F2A1E]/60 font-medium mt-1">
                  Showing {displayedServices.length} verified services managed live in the database.
                </p>
              </div>

              {/* View mode & Sort controls */}
              <div className="flex items-center gap-3">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-[#F2EDE1] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-bold text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20"
                >
                  <option value="default">Default Sorting</option>
                  <option value="price_asc">Price: Low to High</option>
                  <option value="price_desc">Price: High to Low</option>
                  <option value="name">Service Name (A-Z)</option>
                </select>

                <div className="flex items-center bg-[#F2EDE1] p-1 rounded-xl border border-[#E5DEC9]">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-1.5 rounded-lg transition-colors cursor-pointer ${viewMode === 'grid' ? 'bg-[#2F5233] text-white shadow-xs' : 'text-[#1F2A1E]/60 hover:text-[#1F2A1E]'}`}
                    title="Grid View"
                  >
                    <LayoutGrid className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-1.5 rounded-lg transition-colors cursor-pointer ${viewMode === 'list' ? 'bg-[#2F5233] text-white shadow-xs' : 'text-[#1F2A1E]/60 hover:text-[#1F2A1E]'}`}
                    title="List View"
                  >
                    <List className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Sister Subcategory Quick Switcher Chips */}
            {selectedCategory && currentSubcategories.length > 0 && (
              <div className="flex items-center gap-2 overflow-x-auto pt-3 border-t border-[#E5DEC9]/60 scrollbar-none">
                <span className="text-[11px] font-bold text-[#1F2A1E]/50 uppercase tracking-wider flex-shrink-0 mr-1 flex items-center gap-1">
                  <Layers className="w-3 h-3 text-[#2F5233]" />
                  Subcategories:
                </span>
                <button
                  onClick={() => handleSelectSubcategory('')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all flex-shrink-0 cursor-pointer ${
                    selectedSubcategory === ''
                      ? 'bg-[#2F5233] text-white shadow-xs'
                      : 'bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E]'
                  }`}
                >
                  All ({currentCategoryObj ? currentCategoryObj.service_count : allServices.length})
                </button>
                {currentSubcategories.map((sub) => {
                  const isSubActive = selectedSubcategory.toLowerCase() === sub.name.toLowerCase();
                  return (
                    <button
                      key={sub.name}
                      onClick={() => handleSelectSubcategory(sub.name)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all flex-shrink-0 cursor-pointer ${
                        isSubActive
                          ? 'bg-[#2F5233] text-white shadow-xs font-bold'
                          : 'bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#1F2A1E]'
                      }`}
                    >
                      {sub.name} ({sub.service_count})
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Loading or Empty State */}
          {servicesLoading ? (
            <div className="flex items-center justify-center py-20 bg-white rounded-3xl border border-[#E5DEC9]">
              <SmartServeLoader size="md" text="Fetching verified services from database..." />
            </div>
          ) : displayedServices.length === 0 ? (
            <div className="py-16 text-center bg-white rounded-3xl border border-[#E5DEC9] shadow-2xs space-y-3">
              <FolderTree className="w-10 h-10 text-[#1F2A1E]/40 mx-auto" />
              <h3 className="font-serif text-xl font-normal text-[#1F2A1E]">No Services Found</h3>
              <p className="text-xs text-[#1F2A1E]/60 font-medium">No services match your active filters or search terms.</p>
              <button
                onClick={handleResetToCategories}
                className="inline-flex items-center gap-2 px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white rounded-xl text-xs font-bold mt-2 cursor-pointer"
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
                    onClick={() => navigate(`/catalog/service/${svc.id}`)}
                    className="group bg-white rounded-3xl border border-[#E5DEC9] shadow-2xs hover:shadow-lg hover:border-[#2F5233]/40 transition-all cursor-pointer flex flex-col justify-between overflow-hidden"
                  >
                    {/* Real Service Image Cover */}
                    <div className="relative w-full h-44 bg-[#F2EDE1] overflow-hidden">
                      <img
                        src={serviceImg}
                        alt={svc.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        loading="lazy"
                        onError={(e) => {
                          e.currentTarget.onerror = null;
                          e.currentTarget.src = DEFAULT_SERVICE_IMAGE;
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-[#1F2A1E]/70 via-transparent to-transparent" />

                      {/* Top Badges: Rating & Duration */}
                      <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-xs text-white text-[11px] font-bold">
                          <Star className="w-3 h-3 text-[#C9A15A] fill-[#C9A15A]" />
                          <span>{svc.rating || 4.8}</span>
                        </span>

                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-xs text-white text-[11px] font-bold">
                          <Clock className="w-3 h-3 text-[#FAF7F0]/80" />
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
                        <div className="flex items-center gap-1.5 text-[10px] font-bold text-[#2F5233] uppercase tracking-wider">
                          <span>{formatCategoryDisplayName(svc.category)}</span>
                        </div>
                        <h3 className="font-bold text-[#1F2A1E] text-base group-hover:text-[#2F5233] transition-colors line-clamp-1 mt-0.5">
                          {svc.name}
                        </h3>
                        {svc.description && (
                          <p className="text-xs text-[#1F2A1E]/65 font-normal line-clamp-2 mt-1 leading-relaxed">
                            {svc.description}
                          </p>
                        )}
                      </div>

                      {/* Included Feature Highlights Preview */}
                      {featuresPreview.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-[#E5DEC9]/50 text-xs text-[#1F2A1E]/75 font-medium">
                          {featuresPreview.map((f, i) => (
                            <div key={i} className="flex items-center gap-1.5 truncate">
                              <Check className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
                              <span className="truncate">{f}</span>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Pricing & Booking Footer */}
                      <div className="pt-3 border-t border-[#E5DEC9]/60 flex items-center justify-between gap-3">
                        <div>
                          <span className="text-[10px] font-bold text-[#1F2A1E]/45 uppercase tracking-wider block">Price</span>
                          <span className="font-serif text-xl font-normal text-[#1F2A1E]">
                            {formatCurrencyINR(svc.base_price)}
                          </span>
                        </div>

                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/catalog/service/${svc.id}`);
                          }}
                          className="px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white rounded-xl text-xs font-bold transition-all shadow-xs cursor-pointer"
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
                    onClick={() => navigate(`/catalog/service/${svc.id}`)}
                    className="group bg-white p-4 sm:p-5 rounded-3xl border border-[#E5DEC9] shadow-2xs hover:shadow-md hover:border-[#2F5233]/40 transition-all cursor-pointer flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4"
                  >
                    <div className="flex items-center gap-4">
                      <img
                        src={serviceImg}
                        alt={svc.name}
                        className="w-20 h-20 rounded-2xl object-cover flex-shrink-0 bg-[#F2EDE1]"
                        onError={(e) => {
                          e.currentTarget.onerror = null;
                          e.currentTarget.src = DEFAULT_SERVICE_IMAGE;
                        }}
                      />
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-[#2F5233] bg-[#2F5233]/10 px-2.5 py-0.5 rounded-lg">
                            {svc.subcategory}
                          </span>
                          <span className="text-xs font-semibold text-[#1F2A1E]/50">
                            {formatCategoryDisplayName(svc.category)}
                          </span>
                        </div>
                        <h3 className="font-bold text-[#1F2A1E] text-base group-hover:text-[#2F5233] transition-colors">
                          {svc.name}
                        </h3>
                        {svc.description && (
                          <p className="text-xs text-[#1F2A1E]/65 font-normal line-clamp-1 max-w-xl">
                            {svc.description}
                          </p>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center justify-between sm:justify-end gap-6 pt-3 sm:pt-0 border-t sm:border-t-0 border-[#E5DEC9]/60 flex-shrink-0">
                      <div className="text-left sm:text-right">
                        <span className="font-serif text-lg font-normal text-[#1F2A1E] block">
                          {formatCurrencyINR(svc.base_price)}
                        </span>
                        <span className="text-xs font-semibold text-[#1F2A1E]/60">
                          {svc.duration_minutes || 45} Mins
                        </span>
                      </div>

                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/catalog/service/${svc.id}`);
                        }}
                        className="px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white rounded-xl text-xs font-bold transition-all shadow-xs cursor-pointer"
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
