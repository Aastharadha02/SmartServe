import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ChevronRight, 
  Loader2, 
  AlertCircle, 
  Sparkles, 
  Save, 
  CheckCircle2, 
  XCircle, 
  Plus, 
  Trash2, 
  FolderTree, 
  ArrowLeft,
  ArrowUp,
  ArrowDown,
  Check,
  X,
  Wrench,
  Package,
  Layers,
  Image as ImageIcon,
  Eye,
  Clock,
  ShieldCheck,
  HelpCircle,
  AlertTriangle,
  FileText,
  ListCheck,
  RotateCcw,
  Lock,
  History
} from 'lucide-react';
import { getCatalogServices, updateCatalogService, generateAiMetadata, formatRupee, getServiceAuditLogs } from '../../../api/catalog';
import type { ServiceItem, AiMetadataResponse, AuditLogItem } from '../../../api/catalog';
import { getServiceIcon } from '../../../utils/catalogIcons';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';
import { getServiceImage } from '../../../utils/serviceImages';

export const ServiceDetailEditView: React.FC = () => {
  const { serviceId } = useParams<{ serviceId: string }>();
  const navigate = useNavigate();

  const [service, setService] = useState<ServiceItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [saveLoading, setSaveLoading] = useState<boolean>(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveToast, setSaveToast] = useState<string | null>(null);
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  const canEditCatalog = hasPermission(adminSession, 'catalog:edit') || hasPermission(adminSession, 'catalog:manage');
  const canManageCatalog = canEditCatalog;

  // Form Fields State (Readable Typography font sizes)
  const [name, setName] = useState<string>('');
  const [category, setCategory] = useState<string>('');
  const [subcategory, setSubcategory] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [basePrice, setBasePrice] = useState<number>(0);
  const [maxSurge, setMaxSurge] = useState<number>(0.5);
  const [maxDiscount, setMaxDiscount] = useState<number>(0.3);
  const [isActive, setIsActive] = useState<boolean>(true);
  const [estimatedDuration, setEstimatedDuration] = useState<number>(45);

  // 12 Structured Content Sections State
  const [highlights, setHighlights] = useState<string[]>([]);
  const [included, setIncluded] = useState<string[]>([]);
  const [excluded, setExcluded] = useState<string[]>([]);
  const [processSteps, setProcessSteps] = useState<Array<{
    step_number: number;
    title: string;
    description: string;
    duration_minutes?: number;
    is_key_step?: boolean;
  }>>([]);
  const [toolsMaterials, setToolsMaterials] = useState<string[]>([]);
  const [customerSetup, setCustomerSetup] = useState<string[]>([]);
  const [aftercare, setAftercare] = useState<string[]>([]);
  const [expectedResults, setExpectedResults] = useState<string[]>([]);
  const [importantNotes, setImportantNotes] = useState<string[]>([]);
  const [warranty, setWarranty] = useState<string | null>(null);
  const [seoTitle, setSeoTitle] = useState<string>('');
  const [seoDescription, setSeoDescription] = useState<string>('');
  const [keywords, setKeywords] = useState<string[]>([]);
  const [newKeywordInput, setNewKeywordInput] = useState<string>('');
  const [newHighlightInput, setNewHighlightInput] = useState<string>('');
  const [serviceFeatures, setServiceFeatures] = useState<Array<{ title: string; description: string }>>([]);
  const [faqs, setFaqs] = useState<Array<{ question: string; answer: string }>>([]);
  const [serviceMedia, setServiceMedia] = useState<Array<{ id: string; url: string; caption: string; media_type: string; is_cover: boolean }>>([]);
  const [deactivateModalOpen, setDeactivateModalOpen] = useState<boolean>(false);
  const [unavailabilityReason, setUnavailabilityReason] = useState<string>('');
  const [previewModalOpen, setPreviewModalOpen] = useState<boolean>(false);

  // Audit Logs State
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  const [auditFilter, setAuditFilter] = useState<string>('all');
  const [auditLoading, setAuditLoading] = useState<boolean>(false);

  // AI Confirmation & Review Modals State
  const [aiLoading, setAiLoading] = useState<boolean>(false);
  const [confirmRegenerateOpen, setConfirmRegenerateOpen] = useState<boolean>(false);
  const [aiReviewOpen, setAiReviewOpen] = useState<boolean>(false);
  const [aiGeneratedData, setAiGeneratedData] = useState<AiMetadataResponse | null>(null);

  const fetchServiceData = async () => {
    setLoading(true);
    setError(null);
    try {
      const services = await getCatalogServices();
      const match = services.find((s) => s.id === serviceId);
      if (!match) {
        setError('Service item not found in catalog.');
        return;
      }
      setService(match);
      setName(match.name);
      setCategory(match.category);
      setSubcategory(match.subcategory);
      setBasePrice(match.base_price);
      setMaxSurge(match.max_demand_increase);
      setMaxDiscount(match.max_discount);
      setIsActive(match.is_active);

      // Initialize with existing data or trigger AI metadata if empty
      const isPedicure = match.name.toLowerCase().includes('pedicure');
      const isHaircut = match.name.toLowerCase().includes('haircut') || match.name.toLowerCase().includes('hair');
      const isPlumbing = match.category.toLowerCase().includes('plumb') || match.name.toLowerCase().includes('leak');
      const isElectrical = match.category.toLowerCase().includes('electric') || match.name.toLowerCase().includes('switch');

      if (isPedicure) {
        setDescription('Relaxing foot care treatment including soaking, nail trimming, cuticle care, exfoliation, and foot massage.');
        setHighlights(['Hygienic disposable tools', 'Deep foot exfoliation', 'Relaxing foot massage']);
        setIncluded(['Foot soaking in warm solution', 'Nail trimming and shaping', 'Cuticle care', 'Foot exfoliation', 'Dead skin/callus care', 'Foot massage', 'Nail buffing']);
        setExcluded(['Nail extensions (Acrylic/Gel)', 'Nail art', 'Medical treatment of foot conditions']);
        setProcessSteps([
          { step_number: 1, title: 'Foot Inspection', description: 'Check skin and nail condition before treatment.', duration_minutes: 5, is_key_step: false },
          { step_number: 2, title: 'Foot Soaking', description: 'Soak feet in warm soothing bath solution.', duration_minutes: 10, is_key_step: true },
          { step_number: 3, title: 'Nail Trimming & Shaping', description: 'Trim toenails to desired length and shape edges.', duration_minutes: 10, is_key_step: false },
          { step_number: 4, title: 'Cuticle Care & Exfoliation', description: 'Gently push cuticles and scrub dead skin.', duration_minutes: 10, is_key_step: true },
          { step_number: 5, title: 'Foot Massage & Buffing', description: 'Apply moisturizing cream with relaxing foot massage and buff nails.', duration_minutes: 10, is_key_step: true }
        ]);
        setToolsMaterials(['Nail clipper', 'Nail file', 'Cuticle pusher', 'Foot soak basin', 'Foot scrub', 'Pumice stone', 'Nail buffer', 'Foot cream', 'Clean towels']);
        setCustomerSetup([]);
        setAftercare(['Keep feet clean and moisturized daily', 'Avoid tight footwear immediately after polish application']);
        setExpectedResults(['Cleaner and neatly shaped nails', 'Softer skin texture', 'Reduced surface-level dead skin']);
        setWarranty(null); // NULL WARRANTY FOR PEDICURE!
        setFaqs([
          { question: 'Is nail polish included?', answer: 'Standard nail buffing/polish is included. Gel or nail art requires add-on selection.' },
          { question: 'How long does a pedicure take?', answer: 'Standard duration is approximately 45 minutes.' }
        ]);
      } else if (isHaircut) {
        setDescription('Professional hair consultation, precision haircutting, and finishing styling.');
        setHighlights(['Personalized hair consultation', 'Precision haircutting', 'Post-cut styling']);
        setIncluded(['Hair consultation & style assessment', 'Precision haircutting', 'Basic post-cut blow dry & styling', 'Sanitized tools & disposable cape']);
        setExcluded(['Hair wash / shampooing (available as add-on)', 'Hair coloring / chemical treatments', 'Hair spa treatments']);
        setProcessSteps([
          { step_number: 1, title: 'Style Consultation', description: 'Discuss desired hair length and style preference.', duration_minutes: 5, is_key_step: true },
          { step_number: 2, title: 'Hair Sectioning', description: 'Section hair evenly for precision cutting.', duration_minutes: 5, is_key_step: false },
          { step_number: 3, title: 'Haircut Execution', description: 'Perform haircut according to agreed style.', duration_minutes: 20, is_key_step: true },
          { step_number: 4, title: 'Styling & Final Review', description: 'Blow dry, style, and review finished cut with customer.', duration_minutes: 10, is_key_step: true }
        ]);
        setToolsMaterials(['Styling shears', 'Thinning scissors', 'Cutting combs', 'Sectioning clips', 'Water spray bottle', 'Disposable cape']);
        setCustomerSetup(['Please ensure hair is pre-washed and free of heavy styling products']);
        setAftercare(['Use recommended shampoo and styling products to maintain shape']);
        setExpectedResults(['Neat, well-defined haircut matching customer preference']);
        setWarranty(null);
        setFaqs([
          { question: 'Is hair wash included?', answer: 'Basic haircutting is included; hair wash can be added as a separate service option.' }
        ]);
      } else if (isElectrical) {
        setDescription('Safe electrical switchbox installation, wiring check, and load testing by certified electrician.');
        setHighlights(['Power isolation safety check', 'Certified electrical technician', 'Terminal voltage testing']);
        setIncluded(['Site inspection and power isolation', 'Existing wiring safety assessment', 'Switchbox mounting & terminal wiring', 'Voltage & continuity testing']);
        setExcluded(['Supply of new switchboard hardware (unless purchased separately)', 'Heavy main distribution panel rewiring']);
        setProcessSteps([
          { step_number: 1, title: 'Site Inspection & Power Isolation', description: 'Inspect installation area and isolate main circuit breaker for safety.', duration_minutes: 10, is_key_step: true },
          { step_number: 2, title: 'Wiring Assessment & Prep', description: 'Check existing wire gauges and prepare terminal connections.', duration_minutes: 10, is_key_step: false },
          { step_number: 3, title: 'Switchbox Installation', description: 'Securely mount switchbox and connect electrical terminals.', duration_minutes: 20, is_key_step: true },
          { step_number: 4, title: 'Voltage & Continuity Testing', description: 'Restore power and verify voltage output across all switches.', duration_minutes: 10, is_key_step: true }
        ]);
        setToolsMaterials(['Insulated screwdriver set', 'Digital multimeter', 'Wire strippers', 'Electrical insulation tape', 'Voltage detector pen']);
        setCustomerSetup(['Ensure access to main MCB power isolation box']);
        setAftercare(['Avoid overloading switchbox beyond recommended amperage capacity']);
        setExpectedResults(['Safe, properly wired and operational electrical switchbox']);
        setWarranty(null);
        setFaqs([
          { question: 'Does the price include spare switches?', answer: 'The service fee covers installation labor; replacement switches are charged separately.' }
        ]);
      } else if (isPlumbing) {
        setDescription('Leak detection, pipe joint sealing, and plumbing fitting repair by experienced plumber.');
        setHighlights(['Leak isolation testing', 'High-grade thread sealing', 'Pressure check post repair']);
        setIncluded(['Plumbing leak inspection & root cause diagnosis', 'Replacing damaged washers / thread seals', 'Tightening pipe joints and fittings', 'Post-repair water flow & leak test']);
        setExcluded(['Concealed pipe excavation / wall breaking', 'Cost of new major replacement pipes or faucets']);
        setProcessSteps([
          { step_number: 1, title: 'Leak Diagnosis', description: 'Inspect plumbing fixture to identify exact leak source.', duration_minutes: 10, is_key_step: true },
          { step_number: 2, title: 'Water Supply Isolation', description: 'Turn off local stopcock valve to halt water flow.', duration_minutes: 5, is_key_step: false },
          { step_number: 3, title: 'Joint Sealing & Repair', description: 'Replace worn washers and apply Teflon thread sealant tape.', duration_minutes: 25, is_key_step: true },
          { step_number: 4, title: 'Pressure & Leak Testing', description: 'Re-open water valve and verify zero leakage under full pressure.', duration_minutes: 10, is_key_step: true }
        ]);
        setToolsMaterials(['Adjustable pipe wrench', 'Plier set', 'Teflon thread tape', 'Replacement rubber washers', 'Silicone sealant']);
        setCustomerSetup(['Locate and ensure access to main water valve / stopcock']);
        setAftercare(['Monitor repaired joint for 24 hours to ensure complete seal']);
        setExpectedResults(['Completely sealed plumbing joint with zero water leakage']);
        setWarranty(null);
        setFaqs([
          { question: 'What if additional pipe fittings are needed?', answer: 'Technician will inform you of material costs before installing extra parts.' }
        ]);
      } else if (match.name.toLowerCase().includes('cook') || match.category.toLowerCase().includes('food') || match.category.toLowerCase().includes('chef')) {
        setDescription(`Fresh custom ${match.name} preparation at home by experienced cook following dietary preferences.`);
        setHighlights(['Fresh custom meal prep', 'Dietary allergy compliance', 'Kitchen surface cleanup']);
        setIncluded(['Ingredient preparation & chopping', 'Custom dish cooking according to taste preferences', 'Post-cooking stove & counter cleanup']);
        setExcluded(['Groceries & raw ingredient supply (customer provided)', 'Deep dishwashing / sink unclogging']);
        setProcessSteps([
          { step_number: 1, title: 'Menu & Recipe Review', description: 'Review dishes, spice levels, and dietary preferences.', duration_minutes: 5, is_key_step: true },
          { step_number: 2, title: 'Ingredient Preparation', description: 'Wash, trim, and chop vegetables and raw ingredients.', duration_minutes: 15, is_key_step: false },
          { step_number: 3, title: 'Meal Cooking', description: 'Cook dishes using customer utensils and stovetop.', duration_minutes: 35, is_key_step: true },
          { step_number: 4, title: 'Plating & Kitchen Cleanup', description: 'Serve cooked dishes and clean cooking counter.', duration_minutes: 10, is_key_step: true }
        ]);
        setToolsMaterials(['Chef knife', 'Chopping board', 'Spatula', 'Serving bowls', 'Kitchen aprons']);
        setCustomerSetup(['Provide fresh groceries, oil, spices, and clean cookware']);
        setAftercare(['Refrigerate leftover food within 2 hours of meal completion']);
        setExpectedResults(['Freshly prepared meals cooked to specified taste and hygiene standards']);
        setWarranty(null);
        setFaqs([
          { question: 'Do I need to supply ingredients?', answer: 'Yes, customer provides raw ingredients, oil, and spices.' },
          { question: 'Can I specify spice levels?', answer: 'Yes, inform the chef about spice preferences before cooking begins.' }
        ]);
      } else if (match.name.toLowerCase().includes('panel') || match.category.toLowerCase().includes('carpent') || match.category.toLowerCase().includes('paint')) {
        setDescription(`Precision ${match.name} surface mounting, edge alignment, and joint finishing.`);
        setHighlights(['Wall surface alignment check', 'Secured panel mounting', 'Clean edge joint finishing']);
        setIncluded(['Wall surface measurement & alignment check', 'Panel cutting & surface mounting', 'Corner joint sealing & edge trim fitting']);
        setExcluded(['Major masonry or structural wall reconstruction', 'Electrical outlet rewiring behind panels']);
        setProcessSteps([
          { step_number: 1, title: 'Surface Alignment Check', description: 'Measure wall area and verify surface level accuracy.', duration_minutes: 10, is_key_step: true },
          { step_number: 2, title: 'Panel Sizing & Cutting', description: 'Cut wall panels to exact wall dimensions.', duration_minutes: 15, is_key_step: false },
          { step_number: 3, title: 'Panel Mounting & Fixing', description: 'Apply adhesive/fixings to mount panels securely.', duration_minutes: 30, is_key_step: true },
          { step_number: 4, title: 'Edge Sealing & Inspection', description: 'Seal panel edges and inspect installation finish.', duration_minutes: 15, is_key_step: true }
        ]);
        setToolsMaterials(['Laser level gauge', 'Panel cutter', 'High-tack adhesive', 'Silicone sealant', 'Measuring tape']);
        setCustomerSetup(['Ensure work area is clear of furniture and obstruction']);
        setAftercare(['Allow panel adhesive to cure undisturbed for 24 hours']);
        setExpectedResults(['Properly mounted wall panels with clean finished edge joints']);
        setWarranty('30-Day Installation Guarantee: Covers panel fitting and adhesive bond stability.');
        setFaqs([
          { question: 'Does the price include panel materials?', answer: 'Service covers installation labor; panel materials are supplied by customer or billed separately.' },
          { question: 'How long does installation take?', answer: 'Standard installation takes approximately 60 to 90 minutes depending on wall area.' }
        ]);
      } else {
        setDescription(`Dedicated ${match.name} execution tailored to ${match.category} specifications.`);
        setHighlights([`${match.name} execution`, 'Quality verification', 'Clean completion']);
        setIncluded([`Complete ${match.name} service execution`, 'Initial requirements check', 'Post-service cleanup']);
        setExcluded(['Unrelated home repairs or structural modifications']);
        setProcessSteps([
          { step_number: 1, title: 'Initial Assessment', description: `Check requirements for ${match.name}.`, duration_minutes: 10, is_key_step: true },
          { step_number: 2, title: 'Service Execution', description: `Perform ${match.name} according to service standards.`, duration_minutes: 35, is_key_step: true },
          { step_number: 3, title: 'Final Inspection', description: 'Review completed work with customer.', duration_minutes: 10, is_key_step: false }
        ]);
        setToolsMaterials([]);
        setCustomerSetup(['Provide clear access to the service area']);
        setAftercare(['Follow recommended care guidelines for best results']);
        setExpectedResults([`Completed ${match.name} matching customer specifications`]);
        setWarranty(null);
        setFaqs([
          { question: `How long does ${match.name} take?`, answer: 'Standard duration is approximately 45-60 minutes.' }
        ]);
      }

      // Populate sections from persisted suggested_addons if available
      if (Array.isArray(match.suggested_addons) && match.suggested_addons.length > 0) {
        const faqsObj = match.suggested_addons.find((a: any) => a.type === 'faqs');
        if (faqsObj && Array.isArray(faqsObj.items)) {
          setFaqs(faqsObj.items);
        }
        const procObj = match.suggested_addons.find((a: any) => a.type === 'process_steps');
        if (procObj && Array.isArray(procObj.steps)) {
          setProcessSteps(procObj.steps);
        }
        const excObj = match.suggested_addons.find((a: any) => a.type === 'excluded_scope');
        if (excObj && Array.isArray(excObj.items)) {
          setExcluded(excObj.items);
        }
        const tmObj = match.suggested_addons.find((a: any) => a.type === 'tools_materials');
        if (tmObj && Array.isArray(tmObj.tools)) {
          setToolsMaterials(tmObj.tools);
        }
        const csObj = match.suggested_addons.find((a: any) => a.type === 'customer_setup');
        if (csObj && Array.isArray(csObj.requirements)) {
          setCustomerSetup(csObj.requirements);
        }
        const acObj = match.suggested_addons.find((a: any) => a.type === 'aftercare_precautions');
        if (acObj && Array.isArray(acObj.aftercare)) {
          setAftercare(acObj.aftercare);
        }
        const erObj = match.suggested_addons.find((a: any) => a.type === 'expected_results');
        if (erObj && Array.isArray(erObj.items)) {
          setExpectedResults(erObj.items);
        }
        const inObj = match.suggested_addons.find((a: any) => a.type === 'important_notes');
        if (inObj && Array.isArray(inObj.items)) {
          setImportantNotes(inObj.items);
        }
        const wObj = match.suggested_addons.find((a: any) => a.type === 'warranty');
        if (wObj) {
          setWarranty(wObj.has_warranty ? (wObj.details || 'Warranty coverage details') : null);
        }
        const seoObj = match.suggested_addons.find((a: any) => a.type === 'seo_metadata');
        if (seoObj) {
          if (seoObj.seo_title) setSeoTitle(seoObj.seo_title);
          if (seoObj.seo_description) setSeoDescription(seoObj.seo_description);
          if (Array.isArray(seoObj.keywords)) setKeywords(seoObj.keywords);
          if (Array.isArray(seoObj.highlights)) setHighlights(seoObj.highlights);
        }
        const sfObj = match.suggested_addons.find((a: any) => a.type === 'service_features');
        if (sfObj && Array.isArray(sfObj.items)) {
          setServiceFeatures(sfObj.items);
        }
        const smObj = match.suggested_addons.find((a: any) => a.type === 'service_media');
        if (smObj && Array.isArray(smObj.items)) {
          setServiceMedia(smObj.items);
        }

        try {
          setAuditLoading(true);
          const logs = await getServiceAuditLogs(match.id);
          setAuditLogs(logs);
        } catch (logErr) {
          console.error('Audit log fetch error:', logErr);
        } finally {
          setAuditLoading(false);
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load service details.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});
    if (serviceId) {
      fetchServiceData();
    }
  }, [serviceId]);

  const handleSaveChanges = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!service) return;
    if (!canManageCatalog) {
      setSaveError("Permission Denied: Modifying catalog services requires Operations Admin ('catalog:manage') or Super Admin role.");
      return;
    }

    setSaveError(null);
    setSaveLoading(true);

    const structuredAddons: any[] = [
      { type: 'service_media', items: serviceMedia },
      { type: 'service_features', items: serviceFeatures },
      { type: 'seo_metadata', seo_title: seoTitle, seo_description: seoDescription, keywords: keywords, highlights: highlights },
      { type: 'excluded_scope', items: excluded },
      { type: 'process_steps', steps: processSteps },
      { type: 'tools_materials', tools: toolsMaterials, materials: customerSetup },
      { type: 'customer_setup', requirements: customerSetup },
      { type: 'aftercare_precautions', aftercare: aftercare },
      { type: 'expected_results', items: expectedResults },
      { type: 'important_notes', items: importantNotes },
      { type: 'warranty', has_warranty: !!(warranty && warranty.trim()), details: warranty },
      { type: 'faqs', items: faqs }
    ];

    try {
      const updated = await updateCatalogService(service.id, {
        name,
        category,
        subcategory,
        base_price: basePrice,
        max_demand_increase: maxSurge,
        max_discount: maxDiscount,
        is_active: isActive,
        distinct_features: included,
        suggested_addons: structuredAddons,
      });

      setService(updated);
      setSaveToast('Service changes persisted to backend database successfully!');
      setTimeout(() => setSaveToast(null), 4000);

      try {
        const freshLogs = await getServiceAuditLogs(updated.id);
        setAuditLogs(freshLogs);
      } catch (e) {}
    } catch (err: any) {
      const backendDetail = err.response?.data?.detail;
      const msg = typeof backendDetail === 'string' ? backendDetail : 'Failed to save service updates. Please verify input fields.';
      setSaveError(msg);
    } finally {
      setSaveLoading(false);
    }
  };

  // Explicit AI Regeneration Confirmation Flow
  const handleRegenerateClick = () => {
    setConfirmRegenerateOpen(true);
  };

  const handleConfirmRegenerate = async () => {
    setConfirmRegenerateOpen(false);
    if (!service) return;
    setAiLoading(true);
    try {
      const meta = await generateAiMetadata(service.id);
      setAiGeneratedData(meta);
      setAiReviewOpen(true);
    } catch (err: any) {
      setSaveError('AI Metadata generation failed. Ensure backend AI service is active.');
    } finally {
      setAiLoading(false);
    }
  };

  const handleApplyAiData = () => {
    if (!aiGeneratedData) return;

    if (aiGeneratedData.description) setDescription(aiGeneratedData.description);
    if (aiGeneratedData.highlights && aiGeneratedData.highlights.length > 0) setHighlights(aiGeneratedData.highlights);
    if (aiGeneratedData.included && aiGeneratedData.included.length > 0) setIncluded(aiGeneratedData.included);
    if (aiGeneratedData.excluded && aiGeneratedData.excluded.length > 0) setExcluded(aiGeneratedData.excluded);
    if (aiGeneratedData.process_steps && aiGeneratedData.process_steps.length > 0) {
      setProcessSteps(aiGeneratedData.process_steps);
    } else if (aiGeneratedData.how_it_works && aiGeneratedData.how_it_works.length > 0) {
      setProcessSteps(aiGeneratedData.how_it_works);
    }
    if (aiGeneratedData.tools_materials && aiGeneratedData.tools_materials.length > 0) {
      setToolsMaterials(aiGeneratedData.tools_materials);
    } else if (aiGeneratedData.required_tools && aiGeneratedData.required_tools.length > 0) {
      setToolsMaterials(aiGeneratedData.required_tools);
    }
    if (aiGeneratedData.customer_setup) setCustomerSetup(aiGeneratedData.customer_setup);
    if (aiGeneratedData.aftercare) setAftercare(aiGeneratedData.aftercare);
    if (aiGeneratedData.expected_results) setExpectedResults(aiGeneratedData.expected_results);
    setWarranty(aiGeneratedData.warranty || null);
    if (aiGeneratedData.faqs && aiGeneratedData.faqs.length > 0) {
      setFaqs(aiGeneratedData.faqs.map((f: any) => ({
        question: f.question || f.q || '',
        answer: f.answer || f.a || ''
      })));
    }

    setAiReviewOpen(false);
    setSaveToast('Validated AI content applied to form! Click [Save Changes] to persist.');
    setTimeout(() => setSaveToast(null), 4000);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Loader2 className="w-10 h-10 animate-spin text-[#5CA8FF]" />
        <p className="text-base font-semibold text-slate-700">Loading SmartServe Service Management Details...</p>
      </div>
    );
  }

  if (error || !service) {
    return (
      <div className="max-w-3xl mx-auto my-12 p-8 bg-white border border-red-200 rounded-3xl shadow-sm text-center space-y-4">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto" />
        <h3 className="text-xl font-bold text-slate-900">Service Management Error</h3>
        <p className="text-sm text-slate-600 max-w-lg mx-auto">{error || 'Service item not found.'}</p>
        <button
          onClick={() => navigate('/admin/catalog')}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#5CA8FF] text-white rounded-2xl text-sm font-bold shadow-sm"
        >
          <FolderTree className="w-4 h-4" />
          <span>Back to Catalog Categories</span>
        </button>
      </div>
    );
  }

  const ServiceIcon = getServiceIcon(name, category);

  return (
    <div className="space-y-8 max-w-6xl mx-auto font-sans text-slate-800 pb-24">
      {/* Toast Notification */}
      {saveToast && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-3 px-5 py-3.5 bg-slate-900 text-white rounded-2xl shadow-xl border border-slate-700 text-sm font-bold animate-in fade-in">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span>{saveToast}</span>
        </div>
      )}

      {/* Clickable Breadcrumbs Navigation */}
      <nav className="flex items-center gap-2 text-xs text-slate-500 font-medium overflow-x-auto whitespace-nowrap">
        <Link to="/admin/catalog" className="hover:text-[#5CA8FF] flex items-center gap-1 transition-colors flex-shrink-0">
          <FolderTree className="w-3.5 h-3.5" />
          <span>Catalog</span>
        </Link>
        <ChevronRight className="w-4 h-4 text-slate-300 flex-shrink-0" />
        <Link to={`/admin/catalog/category/${encodeURIComponent(category)}`} className="hover:text-[#5CA8FF] transition-colors flex-shrink-0">
          {category}
        </Link>
        <ChevronRight className="w-4 h-4 text-slate-300 flex-shrink-0" />
        <Link to={`/admin/catalog/category/${encodeURIComponent(category)}/subcategory/${encodeURIComponent(subcategory)}`} className="hover:text-[#5CA8FF] transition-colors flex-shrink-0">
          {subcategory}
        </Link>
        <ChevronRight className="w-4 h-4 text-slate-300 flex-shrink-0" />
        <span className="text-slate-900 font-bold flex-shrink-0 truncate max-w-xs">{name}</span>
      </nav>

      {/* Page Title & Header Banner */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 sm:gap-6 bg-white p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl border border-slate-200 shadow-sm">
        <div className="flex items-start sm:items-center gap-3 sm:gap-5 min-w-0">
          <button
            onClick={() => navigate(`/admin/catalog/category/${encodeURIComponent(category)}/subcategory/${encodeURIComponent(subcategory)}`)}
            className="p-2.5 sm:p-3 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors flex-shrink-0"
            title="Back to Subcategory Services"
          >
            <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
          <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl overflow-hidden bg-slate-100 border border-slate-200 flex-shrink-0 shadow-2xs">
            <img
              src={getServiceImage(category, name)}
              alt={name}
              className="w-full h-full object-cover"
            />
          </div>
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2 sm:gap-3">
              <h1 className="text-xl sm:text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight truncate">{name}</h1>
              <span className="text-base sm:text-xl font-extrabold text-slate-900 font-mono bg-blue-50 text-[#2563EB] px-3 py-1 rounded-xl border border-blue-100">
                {formatRupee(basePrice)}
              </span>
              {isActive ? (
                <span className="inline-flex items-center gap-1.5 px-3 py-0.5 sm:py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs sm:text-sm font-bold shadow-xs">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  Active
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 px-3 py-0.5 sm:py-1 rounded-full bg-rose-50 text-rose-700 border border-rose-200 text-xs sm:text-sm font-bold shadow-xs">
                  <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                  Inactive
                </span>
              )}
            </div>
            <p className="text-xs sm:text-sm text-slate-500 font-semibold mt-1 truncate">
              Category: <span className="text-slate-800 font-bold">{category}</span> • Subcategory: <span className="text-slate-800 font-bold">{subcategory}</span>
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2 sm:gap-3 w-full lg:w-auto">
          <button
            type="button"
            onClick={() => setPreviewModalOpen(true)}
            className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 sm:px-5 py-2.5 sm:py-3 bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 font-bold text-xs sm:text-sm rounded-2xl shadow-xs transition-colors"
          >
            <Eye className="w-4 h-4 text-[#5CA8FF]" />
            <span>Preview</span>
          </button>

          {canManageCatalog ? (
            <>
              <button
                onClick={handleRegenerateClick}
                disabled={aiLoading}
                className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 sm:px-5 py-2.5 sm:py-3 bg-blue-50 hover:bg-blue-100 text-[#5CA8FF] border border-blue-200 font-bold text-xs sm:text-sm rounded-2xl transition-colors disabled:opacity-50"
              >
                {aiLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RotateCcw className="w-4 h-4" />}
                <span>AI Content</span>
              </button>

              <button
                onClick={handleSaveChanges}
                disabled={saveLoading}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-5 sm:px-6 py-2.5 sm:py-3 bg-[#5CA8FF] hover:bg-blue-600 text-white font-bold text-xs sm:text-sm rounded-2xl shadow-sm transition-colors disabled:opacity-50"
              >
                {saveLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4 sm:w-5 sm:h-5" />}
                <span>Save Changes</span>
              </button>
            </>
          ) : (
            <button
              disabled
              title="Modifying catalog services requires Operations Admin ('catalog:manage') or Super Admin role."
              className="w-full sm:w-auto flex items-center justify-center gap-2 px-5 sm:px-6 py-2.5 sm:py-3 bg-slate-200 text-slate-500 font-bold text-xs sm:text-sm rounded-2xl cursor-not-allowed opacity-70 border border-slate-300"
            >
              <Save className="w-4 h-4 sm:w-5 sm:h-5 text-slate-400" />
              <span>Save Changes (View Only)</span>
            </button>
          )}
        </div>
      </div>

      {/* Save Error Banner (Dismissible, Non-alert) */}
      {saveError && (
        <div className="p-5 bg-red-50 border border-red-200 text-red-800 rounded-3xl text-sm font-bold flex items-center justify-between animate-in fade-in shadow-sm">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
            <span>{saveError}</span>
          </div>
          <button onClick={() => setSaveError(null)} className="text-red-500 hover:text-red-800 p-1">
            <X className="w-5 h-5" />
          </button>
        </div>
      )}

      <form onSubmit={handleSaveChanges} className="space-y-8">
        {!canManageCatalog && (
          <div className="p-4 bg-amber-50 border border-amber-200 rounded-3xl text-amber-900 text-sm font-bold flex items-center gap-3 shadow-xs">
            <Lock className="w-5 h-5 text-amber-600 flex-shrink-0" />
            <span>
              🔒 <strong>View-Only Mode:</strong> You are inspecting catalog service details in read-only mode. Modifying service fields or pricing requires Operations Admin ('catalog:manage') or Super Admin role.
            </span>
          </div>
        )}
        
        {/* Section 1: Basic Information */}
        <div className="bg-white p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl border border-slate-200 shadow-sm space-y-4 sm:space-y-5">
          <div className="border-b border-slate-100 pb-3 sm:pb-4">
            <h2 className="text-lg sm:text-xl font-bold text-slate-900">1. Basic Information</h2>
            <p className="text-xs sm:text-sm text-slate-500 font-semibold">Service identification and catalog status</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-5 text-sm">
            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Service Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={!canManageCatalog}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 font-bold text-slate-900 text-base focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Category</label>
              <input
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                disabled={!canManageCatalog}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 font-semibold text-slate-800 text-base focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Subcategory</label>
              <input
                type="text"
                value={subcategory}
                onChange={(e) => setSubcategory(e.target.value)}
                disabled={!canManageCatalog}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 font-semibold text-slate-800 text-base focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                required
              />
            </div>
          </div>

          <div className="flex items-center gap-4 pt-2">
            <button
              type="button"
              onClick={() => setIsActive(!isActive)}
              disabled={!canManageCatalog}
              className={`inline-flex items-center gap-2 px-4 py-2 rounded-2xl text-sm font-bold transition-colors ${
                isActive
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : 'bg-slate-100 text-slate-500 border border-slate-200'
              } ${!canManageCatalog ? 'opacity-75 cursor-not-allowed' : ''}`}
            >
              {isActive ? <CheckCircle2 className="w-5 h-5 text-emerald-500" /> : <XCircle className="w-5 h-5 text-slate-400" />}
              <span>{isActive ? 'Catalog Active (Customers can book)' : 'Catalog Disabled'}</span>
            </button>
          </div>
        </div>

        {/* Section 2: Description & Highlights */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-5">
          <div className="border-b border-slate-100 pb-4">
            <h2 className="text-xl font-bold text-slate-900">2. Service Description & Highlights</h2>
            <p className="text-sm text-slate-500 font-semibold">Service summary and key customer selling points</p>
          </div>

          <div className="space-y-4 text-sm">
            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Service Overview Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={!canManageCatalog}
                rows={3}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-base font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                placeholder="Enter detailed description..."
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="font-bold text-slate-700">Service Highlights & Feature Badges</label>
                <button
                  type="button"
                  onClick={() => setHighlights([...highlights, 'New Service Highlight'])}
                  disabled={!canManageCatalog}
                  className="flex items-center gap-1 px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Add Highlight</span>
                </button>
              </div>

              <div className="space-y-2 bg-slate-50 p-4 rounded-2xl border border-slate-200">
                {highlights.map((h, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <Check className="w-4 h-4 text-[#5CA8FF] flex-shrink-0" />
                    <input
                      type="text"
                      value={h}
                      onChange={(e) => {
                        const copy = [...highlights];
                        copy[i] = e.target.value;
                        setHighlights(copy);
                      }}
                      disabled={!canManageCatalog}
                      className="w-full bg-white border border-slate-200 rounded-xl px-3.5 py-2 text-sm font-semibold disabled:opacity-75 disabled:cursor-not-allowed"
                    />
                    <button
                      type="button"
                      onClick={() => setHighlights(highlights.filter((_, idx) => idx !== i))}
                      disabled={!canManageCatalog}
                      className="text-slate-400 hover:text-red-500 p-1 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Pricing & Limits (Indian Rupee ₹) */}
        <div className="bg-white p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl border border-slate-200 shadow-sm space-y-4 sm:space-y-5">
          <div className="border-b border-slate-100 pb-3 sm:pb-4">
            <h2 className="text-lg sm:text-xl font-bold text-slate-900">3. Rate Controls (Indian Rupee ₹)</h2>
            <p className="text-xs sm:text-sm text-slate-500 font-semibold">Base rate in ₹, duration, and dynamic pricing limits</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 text-sm">
            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Base Price in ₹</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 font-bold text-slate-400 font-mono text-base">₹</span>
                <input
                  type="number"
                  step="1"
                  value={basePrice}
                  onChange={(e) => setBasePrice(parseFloat(e.target.value) || 0)}
                  disabled={!canManageCatalog}
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl pl-9 pr-4 py-3 font-mono font-bold text-slate-900 text-lg focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                  required
                />
              </div>
              <p className="text-xs text-slate-400 mt-1 font-mono">Formatted: {formatRupee(basePrice)}</p>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Estimated Duration (Mins)</label>
              <input
                type="number"
                value={estimatedDuration}
                onChange={(e) => setEstimatedDuration(parseInt(e.target.value) || 30)}
                disabled={!canManageCatalog}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 font-mono text-slate-900 font-bold text-base focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Max Demand Surge Cap</label>
              <input
                type="number"
                step="0.05"
                value={maxSurge}
                onChange={(e) => setMaxSurge(parseFloat(e.target.value) || 0)}
                disabled={!canManageCatalog}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 font-mono text-amber-800 font-bold text-base focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                required
              />
              <p className="text-xs text-amber-700 mt-1 font-mono">+{(maxSurge * 100).toFixed(0)}% Surge</p>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1.5">Max Discount Cap</label>
              <input
                type="number"
                step="0.05"
                value={maxDiscount}
                onChange={(e) => setMaxDiscount(parseFloat(e.target.value) || 0)}
                disabled={!canManageCatalog}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 font-mono text-emerald-800 font-bold text-base focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 disabled:opacity-75 disabled:cursor-not-allowed"
                required
              />
              <p className="text-xs text-emerald-700 mt-1 font-mono">-{(maxDiscount * 100).toFixed(0)}% Discount</p>
            </div>
          </div>
        </div>

        {/* Section 4: INCLUDED vs EXCLUDED */}
        <div className="bg-white p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl border border-slate-200 shadow-sm space-y-5 sm:space-y-6">
          <div className="border-b border-slate-100 pb-3 sm:pb-4">
            <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-slate-900">4. Service Scope Boundaries (Included vs Excluded)</h2>
            <p className="text-xs sm:text-sm md:text-base text-slate-500 font-semibold mt-1">Service-specific scope inclusions and scope exclusions</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 text-base">
            {/* Left Panel: Included */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="font-bold text-emerald-800 flex items-center gap-2 text-base md:text-lg">
                  <CheckCircle2 className="w-6 h-6 text-emerald-600" />
                  <span>WHAT'S INCLUDED ({included.length})</span>
                </label>
                <button
                  type="button"
                  onClick={() => setIncluded([...included, 'New included item'])}
                  disabled={!canEditCatalog}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-100 hover:bg-emerald-200 text-emerald-800 rounded-xl text-xs font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Inclusion</span>
                </button>
              </div>

              <div className="space-y-3 bg-emerald-50/60 p-5 rounded-3xl border border-emerald-200">
                {included.length === 0 ? (
                  <p className="text-sm text-slate-400 font-medium italic text-center py-2">No scope inclusions specified yet.</p>
                ) : (
                  included.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2 bg-white p-2.5 rounded-2xl border border-emerald-200 shadow-xs">
                      <Check className="w-5 h-5 text-emerald-600 flex-shrink-0 ml-1" />
                      <input
                        type="text"
                        value={item}
                        onChange={(e) => {
                          const copy = [...included];
                          copy[idx] = e.target.value;
                          setIncluded(copy);
                        }}
                        disabled={!canEditCatalog}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500/30 disabled:opacity-75 disabled:cursor-not-allowed"
                      />
                      <div className="flex items-center gap-1 flex-shrink-0">
                        <button
                          type="button"
                          disabled={!canEditCatalog || idx === 0}
                          onClick={() => {
                            const copy = [...included];
                            const temp = copy[idx - 1];
                            copy[idx - 1] = copy[idx];
                            copy[idx] = temp;
                            setIncluded(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Up"
                        >
                          <ArrowUp className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          disabled={!canEditCatalog || idx === included.length - 1}
                          onClick={() => {
                            const copy = [...included];
                            const temp = copy[idx + 1];
                            copy[idx + 1] = copy[idx];
                            copy[idx] = temp;
                            setIncluded(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Down"
                        >
                          <ArrowDown className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          disabled={!canEditCatalog}
                          onClick={() => setIncluded(included.filter((_, i) => i !== idx))}
                          className="p-1 text-rose-400 hover:text-rose-600 disabled:opacity-30"
                          title="Delete Inclusion"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Right Panel: Excluded */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="font-bold text-rose-800 flex items-center gap-2 text-base md:text-lg">
                  <XCircle className="w-6 h-6 text-rose-600" />
                  <span>WHAT IS NOT INCLUDED / EXCLUDED ({excluded.length})</span>
                </label>
                <button
                  type="button"
                  onClick={() => setExcluded([...excluded, 'New excluded item'])}
                  disabled={!canEditCatalog}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-rose-100 hover:bg-rose-200 text-rose-800 rounded-xl text-xs font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Exclusion</span>
                </button>
              </div>

              <div className="space-y-3 bg-rose-50/60 p-5 rounded-3xl border border-rose-200">
                {excluded.length === 0 ? (
                  <p className="text-sm text-slate-400 font-medium italic text-center py-2">No scope exclusions specified yet.</p>
                ) : (
                  excluded.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2 bg-white p-2.5 rounded-2xl border border-rose-200 shadow-xs">
                      <X className="w-5 h-5 text-rose-600 flex-shrink-0 ml-1" />
                      <input
                        type="text"
                        value={item}
                        onChange={(e) => {
                          const copy = [...excluded];
                          copy[idx] = e.target.value;
                          setExcluded(copy);
                        }}
                        disabled={!canEditCatalog}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-rose-500/30 disabled:opacity-75 disabled:cursor-not-allowed"
                      />
                      <div className="flex items-center gap-1 flex-shrink-0">
                        <button
                          type="button"
                          disabled={!canEditCatalog || idx === 0}
                          onClick={() => {
                            const copy = [...excluded];
                            const temp = copy[idx - 1];
                            copy[idx - 1] = copy[idx];
                            copy[idx] = temp;
                            setExcluded(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Up"
                        >
                          <ArrowUp className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          disabled={!canEditCatalog || idx === excluded.length - 1}
                          onClick={() => {
                            const copy = [...excluded];
                            const temp = copy[idx + 1];
                            copy[idx + 1] = copy[idx];
                            copy[idx] = temp;
                            setExcluded(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Down"
                        >
                          <ArrowDown className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          disabled={!canEditCatalog}
                          onClick={() => setExcluded(excluded.filter((_, i) => i !== idx))}
                          className="p-1 text-rose-400 hover:text-rose-600 disabled:opacity-30"
                          title="Delete Exclusion"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Section 5: Step-by-Step How It Works Workflow */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900">5. How It Works / Service Execution Process</h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Service-specific operational steps ({processSteps.length} Steps)</p>
            </div>
            <button
              type="button"
              onClick={() => setProcessSteps([...processSteps, {
                step_number: processSteps.length + 1,
                title: 'New Service Step',
                description: 'Step execution details',
                duration_minutes: 15,
                is_key_step: false
              }])}
              className="inline-flex items-center gap-2 px-4 py-2.5 bg-[#5CA8FF] hover:bg-blue-600 text-white rounded-2xl text-xs md:text-sm font-bold shadow-sm transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Process Step</span>
            </button>
          </div>

          <div className="space-y-4">
            {processSteps.length === 0 ? (
              <div className="p-8 text-center bg-slate-50 rounded-3xl border border-slate-200 space-y-3">
                <Clock className="w-8 h-8 text-slate-400 mx-auto" />
                <p className="text-base text-slate-600 font-semibold">No process steps added yet.</p>
                <button
                  type="button"
                  onClick={() => setProcessSteps([{
                    step_number: 1,
                    title: 'Service Initial Assessment',
                    description: 'Initial site check or consultation before starting work.',
                    duration_minutes: 10,
                    is_key_step: true
                  }])}
                  className="px-4 py-2 bg-white border border-slate-300 hover:border-[#5CA8FF] text-[#5CA8FF] rounded-xl text-xs font-bold transition-colors"
                >
                  + Add First Step
                </button>
              </div>
            ) : (
              processSteps.map((step, idx) => (
                <div key={idx} className="p-6 bg-slate-50/70 rounded-3xl border border-slate-200 space-y-4 shadow-xs">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="flex items-center gap-3 flex-1">
                      <span className="w-9 h-9 rounded-full bg-[#5CA8FF] text-white font-bold flex items-center justify-center text-base font-mono flex-shrink-0">
                        {idx + 1}
                      </span>
                      <input
                        type="text"
                        value={step.title}
                        onChange={(e) => {
                          const copy = [...processSteps];
                          copy[idx].title = e.target.value;
                          setProcessSteps(copy);
                        }}
                        placeholder="Step Title..."
                        className="font-bold text-slate-900 bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-base md:text-lg flex-1 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
                        required
                      />
                    </div>

                    <div className="flex items-center gap-4 flex-wrap">
                      <label className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs md:text-sm font-bold text-slate-700 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={step.is_key_step}
                          onChange={(e) => {
                            const copy = [...processSteps];
                            copy[idx].is_key_step = e.target.checked;
                            setProcessSteps(copy);
                          }}
                          className="rounded text-[#5CA8FF] w-4 h-4"
                        />
                        <span className={step.is_key_step ? 'text-[#5CA8FF]' : 'text-slate-600'}>Key Step</span>
                      </label>

                      <div className="flex items-center gap-1.5 bg-white border border-slate-200 rounded-xl px-3 py-1.5 text-slate-700 font-mono text-xs md:text-sm">
                        <Clock className="w-4 h-4 text-slate-400" />
                        <input
                          type="number"
                          min="0"
                          value={step.duration_minutes ?? ''}
                          onChange={(e) => {
                            const copy = [...processSteps];
                            const val = e.target.value === '' ? undefined : Math.max(0, parseInt(e.target.value) || 0);
                            copy[idx].duration_minutes = val;
                            setProcessSteps(copy);
                          }}
                          placeholder="Mins"
                          className="w-16 bg-slate-50 border border-slate-200 rounded-lg px-2 text-center py-1 font-bold text-slate-900"
                        />
                        <span className="font-semibold text-slate-500">mins</span>
                      </div>

                      <div className="flex items-center gap-1">
                        <button
                          type="button"
                          disabled={idx === 0}
                          onClick={() => {
                            const copy = [...processSteps];
                            const temp = copy[idx - 1];
                            copy[idx - 1] = copy[idx];
                            copy[idx] = temp;
                            // Update step_numbers
                            copy.forEach((s, i) => s.step_number = i + 1);
                            setProcessSteps(copy);
                          }}
                          className="p-1.5 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Up"
                        >
                          <ArrowUp className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          disabled={idx === processSteps.length - 1}
                          onClick={() => {
                            const copy = [...processSteps];
                            const temp = copy[idx + 1];
                            copy[idx + 1] = copy[idx];
                            copy[idx] = temp;
                            copy.forEach((s, i) => s.step_number = i + 1);
                            setProcessSteps(copy);
                          }}
                          className="p-1.5 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Down"
                        >
                          <ArrowDown className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            const copy = processSteps.filter((_, i) => i !== idx);
                            copy.forEach((s, i) => s.step_number = i + 1);
                            setProcessSteps(copy);
                          }}
                          className="p-1.5 text-rose-400 hover:text-rose-600"
                          title="Delete Process Step"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>

                  <textarea
                    value={step.description}
                    onChange={(e) => {
                      const copy = [...processSteps];
                      copy[idx].description = e.target.value;
                      setProcessSteps(copy);
                    }}
                    placeholder="Describe step details..."
                    className="w-full bg-white border border-slate-200 rounded-xl p-3.5 text-base text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
                    rows={2}
                    required
                  />
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 6: Tools & Materials / Products */}
        <div className="bg-white p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl border border-slate-200 shadow-sm space-y-5 sm:space-y-6">
          <div className="border-b border-slate-100 pb-3 sm:pb-4">
            <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-slate-900">6. Service Tools & Materials / Consumables</h2>
            <p className="text-xs sm:text-sm md:text-base text-slate-500 font-semibold mt-1">Equipment, specialized tools, and consumables required for this service</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 text-base">
            {/* Left Panel: Tools */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="font-bold text-slate-800 flex items-center gap-2 text-base md:text-lg">
                  <Wrench className="w-6 h-6 text-[#5CA8FF]" />
                  <span>REQUIRED TOOLS ({toolsMaterials.length})</span>
                </label>
                <button
                  type="button"
                  onClick={() => setToolsMaterials([...toolsMaterials, 'New Tool'])}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-[#5CA8FF] border border-blue-200 rounded-xl text-xs font-bold transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Tool</span>
                </button>
              </div>

              <div className="space-y-3 bg-slate-50/70 p-5 rounded-3xl border border-slate-200">
                {toolsMaterials.length === 0 ? (
                  <p className="text-sm text-slate-400 font-medium italic text-center py-2">No tools specified yet.</p>
                ) : (
                  toolsMaterials.map((t, idx) => (
                    <div key={idx} className="flex items-center gap-2 bg-white p-2.5 rounded-2xl border border-slate-200 shadow-xs">
                      <span className="w-2.5 h-2.5 rounded-full bg-[#5CA8FF] ml-1 flex-shrink-0"></span>
                      <input
                        type="text"
                        value={t}
                        onChange={(e) => {
                          const copy = [...toolsMaterials];
                          copy[idx] = e.target.value;
                          setToolsMaterials(copy);
                        }}
                        placeholder="Tool Name..."
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                      />
                      <div className="flex items-center gap-1 flex-shrink-0">
                        <button
                          type="button"
                          disabled={idx === 0}
                          onClick={() => {
                            const copy = [...toolsMaterials];
                            const temp = copy[idx - 1];
                            copy[idx - 1] = copy[idx];
                            copy[idx] = temp;
                            setToolsMaterials(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Up"
                        >
                          <ArrowUp className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          disabled={idx === toolsMaterials.length - 1}
                          onClick={() => {
                            const copy = [...toolsMaterials];
                            const temp = copy[idx + 1];
                            copy[idx + 1] = copy[idx];
                            copy[idx] = temp;
                            setToolsMaterials(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Down"
                        >
                          <ArrowDown className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => setToolsMaterials(toolsMaterials.filter((_, i) => i !== idx))}
                          className="p-1 text-rose-400 hover:text-rose-600"
                          title="Delete Tool"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Right Panel: Materials / Consumables */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="font-bold text-amber-900 flex items-center gap-2 text-base md:text-lg">
                  <Package className="w-6 h-6 text-amber-600" />
                  <span>MATERIALS & CONSUMABLES ({customerSetup.length > 0 ? customerSetup.length : 0})</span>
                </label>
                <button
                  type="button"
                  onClick={() => setCustomerSetup([...customerSetup, 'New Material / Product'])}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 rounded-xl text-xs font-bold transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  <span>Add Material</span>
                </button>
              </div>

              <div className="space-y-3 bg-amber-50/50 p-5 rounded-3xl border border-amber-200">
                {customerSetup.length === 0 ? (
                  <p className="text-sm text-slate-400 font-medium italic text-center py-2">No materials or products specified yet.</p>
                ) : (
                  customerSetup.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2 bg-white p-2.5 rounded-2xl border border-amber-200 shadow-xs">
                      <Layers className="w-4 h-4 text-amber-600 ml-1 flex-shrink-0" />
                      <input
                        type="text"
                        value={item}
                        onChange={(e) => {
                          const copy = [...customerSetup];
                          copy[idx] = e.target.value;
                          setCustomerSetup(copy);
                        }}
                        placeholder="Material / Product Name..."
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500/30"
                      />
                      <div className="flex items-center gap-1 flex-shrink-0">
                        <button
                          type="button"
                          disabled={idx === 0}
                          onClick={() => {
                            const copy = [...customerSetup];
                            const temp = copy[idx - 1];
                            copy[idx - 1] = copy[idx];
                            copy[idx] = temp;
                            setCustomerSetup(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Up"
                        >
                          <ArrowUp className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          disabled={idx === customerSetup.length - 1}
                          onClick={() => {
                            const copy = [...customerSetup];
                            const temp = copy[idx + 1];
                            copy[idx + 1] = copy[idx];
                            copy[idx] = temp;
                            setCustomerSetup(copy);
                          }}
                          className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                          title="Move Down"
                        >
                          <ArrowDown className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => setCustomerSetup(customerSetup.filter((_, i) => i !== idx))}
                          className="p-1 text-rose-400 hover:text-rose-600"
                          title="Delete Material"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Section 7: Customer Preparation & Setup Requirements */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <ListCheck className="w-6 h-6 text-amber-600" />
                <span>7. Customer Preparation & Setup Requirements</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">What the customer needs to prepare or provide before the service ({customerSetup.length} Requirements)</p>
            </div>
            <button
              type="button"
              onClick={() => setCustomerSetup([...customerSetup, 'Customer should clear work area and ensure clear access.'])}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Requirement</span>
            </button>
          </div>

          <div className="space-y-4">
            {customerSetup.length === 0 ? (
              <div className="p-8 text-center bg-slate-50 rounded-3xl border border-slate-200 space-y-3">
                <ListCheck className="w-8 h-8 text-slate-400 mx-auto" />
                <p className="text-base text-slate-600 font-semibold">No special customer preparation required.</p>
                <button
                  type="button"
                  onClick={() => setCustomerSetup(['Customer should ensure clear access to the service location.'])}
                  className="px-4 py-2 bg-white border border-slate-300 hover:border-amber-500 text-amber-800 rounded-xl text-xs font-bold transition-colors"
                >
                  + Add First Requirement
                </button>
              </div>
            ) : (
              customerSetup.map((reqText, idx) => (
                <div key={idx} className="p-5 bg-amber-50/50 rounded-3xl border border-amber-200 space-y-3 shadow-xs">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2 flex-1">
                      <span className="w-2.5 h-2.5 rounded-full bg-amber-600 ml-1 flex-shrink-0"></span>
                      <input
                        type="text"
                        value={reqText}
                        onChange={(e) => {
                          const copy = [...customerSetup];
                          copy[idx] = e.target.value;
                          setCustomerSetup(copy);
                        }}
                        placeholder="Describe customer setup requirement..."
                        className="w-full bg-white border border-amber-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500/30"
                        required
                      />
                    </div>
                    <div className="flex items-center gap-1 flex-shrink-0">
                      <button
                        type="button"
                        disabled={idx === 0}
                        onClick={() => {
                          const copy = [...customerSetup];
                          const temp = copy[idx - 1];
                          copy[idx - 1] = copy[idx];
                          copy[idx] = temp;
                          setCustomerSetup(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Up"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        disabled={idx === customerSetup.length - 1}
                        onClick={() => {
                          const copy = [...customerSetup];
                          const temp = copy[idx + 1];
                          copy[idx + 1] = copy[idx];
                          copy[idx] = temp;
                          setCustomerSetup(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Down"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setCustomerSetup(customerSetup.filter((_, i) => i !== idx))}
                        className="p-1 text-rose-400 hover:text-rose-600"
                        title="Delete Requirement"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 8: Aftercare & Precautions */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <ShieldCheck className="w-6 h-6 text-emerald-600" />
                <span>8. Aftercare & Service Precautions</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Post-service care instructions and safety precautions for the customer ({aftercare.length} Instructions)</p>
            </div>
            <button
              type="button"
              onClick={() => setAftercare([...aftercare, 'Follow post-service care guidelines to maintain results.'])}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Instruction</span>
            </button>
          </div>

          <div className="space-y-4">
            {aftercare.length === 0 ? (
              <div className="p-8 text-center bg-slate-50 rounded-3xl border border-slate-200 space-y-3">
                <ShieldCheck className="w-8 h-8 text-slate-400 mx-auto" />
                <p className="text-base text-slate-600 font-semibold">No specific aftercare instructions.</p>
                <button
                  type="button"
                  onClick={() => setAftercare(['Follow post-service care guidelines.'])}
                  className="px-4 py-2 bg-white border border-slate-300 hover:border-emerald-500 text-emerald-800 rounded-xl text-xs font-bold transition-colors"
                >
                  + Add First Instruction
                </button>
              </div>
            ) : (
              aftercare.map((tip, idx) => (
                <div key={idx} className="p-5 bg-emerald-50/50 rounded-3xl border border-emerald-200 space-y-3 shadow-xs">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2 flex-1">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 ml-1 flex-shrink-0"></span>
                      <input
                        type="text"
                        value={tip}
                        onChange={(e) => {
                          const copy = [...aftercare];
                          copy[idx] = e.target.value;
                          setAftercare(copy);
                        }}
                        placeholder="Describe aftercare instruction or precaution..."
                        className="w-full bg-white border border-emerald-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500/30"
                        required
                      />
                    </div>
                    <div className="flex items-center gap-1 flex-shrink-0">
                      <button
                        type="button"
                        disabled={idx === 0}
                        onClick={() => {
                          const copy = [...aftercare];
                          const temp = copy[idx - 1];
                          copy[idx - 1] = copy[idx];
                          copy[idx] = temp;
                          setAftercare(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Up"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        disabled={idx === aftercare.length - 1}
                        onClick={() => {
                          const copy = [...aftercare];
                          const temp = copy[idx + 1];
                          copy[idx + 1] = copy[idx];
                          copy[idx] = temp;
                          setAftercare(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Down"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setAftercare(aftercare.filter((_, i) => i !== idx))}
                        className="p-1 text-rose-400 hover:text-rose-600"
                        title="Delete Instruction"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 9: Expected Results */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <FileText className="w-6 h-6 text-purple-600" />
                <span>9. Expected Service Results</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Realistic service outcomes the customer can expect ({expectedResults.length} Outcomes)</p>
            </div>
            <button
              type="button"
              onClick={() => setExpectedResults([...expectedResults, 'Expected outcome matching customer specifications.'])}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-purple-50 hover:bg-purple-100 text-purple-900 border border-purple-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Expected Result</span>
            </button>
          </div>

          <div className="space-y-4">
            {expectedResults.length === 0 ? (
              <div className="p-8 text-center bg-slate-50 rounded-3xl border border-slate-200 space-y-3">
                <FileText className="w-8 h-8 text-slate-400 mx-auto" />
                <p className="text-base text-slate-600 font-semibold">No expected results specified.</p>
                <button
                  type="button"
                  onClick={() => setExpectedResults(['Completed service matching customer expectations.'])}
                  className="px-4 py-2 bg-white border border-slate-300 hover:border-purple-500 text-purple-800 rounded-xl text-xs font-bold transition-colors"
                >
                  + Add First Result
                </button>
              </div>
            ) : (
              expectedResults.map((res, idx) => (
                <div key={idx} className="p-5 bg-purple-50/50 rounded-3xl border border-purple-200 space-y-3 shadow-xs">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2 flex-1">
                      <Check className="w-5 h-5 text-purple-600 ml-1 flex-shrink-0" />
                      <input
                        type="text"
                        value={res}
                        onChange={(e) => {
                          const copy = [...expectedResults];
                          copy[idx] = e.target.value;
                          setExpectedResults(copy);
                        }}
                        placeholder="Describe realistic expected outcome..."
                        className="w-full bg-white border border-purple-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-purple-500/30"
                        required
                      />
                    </div>
                    <div className="flex items-center gap-1 flex-shrink-0">
                      <button
                        type="button"
                        disabled={idx === 0}
                        onClick={() => {
                          const copy = [...expectedResults];
                          const temp = copy[idx - 1];
                          copy[idx - 1] = copy[idx];
                          copy[idx] = temp;
                          setExpectedResults(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Up"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        disabled={idx === expectedResults.length - 1}
                        onClick={() => {
                          const copy = [...expectedResults];
                          const temp = copy[idx + 1];
                          copy[idx + 1] = copy[idx];
                          copy[idx] = temp;
                          setExpectedResults(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Down"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setExpectedResults(expectedResults.filter((_, i) => i !== idx))}
                        className="p-1 text-rose-400 hover:text-rose-600"
                        title="Delete Result"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 10: Important Notes */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <AlertTriangle className="w-6 h-6 text-amber-500" />
                <span>10. Important Service Notes</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Genuinely important service-specific disclosures and advisories ({importantNotes.length} Notes)</p>
            </div>
            <button
              type="button"
              onClick={() => setImportantNotes([...importantNotes, 'Important service-specific information advisory.'])}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Note</span>
            </button>
          </div>

          <div className="space-y-4">
            {importantNotes.length === 0 ? (
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-sm">
                <span className="text-slate-500 font-semibold flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-500" />
                  No additional service notes configured.
                </span>
                <button
                  type="button"
                  onClick={() => setImportantNotes(['Inform professional of any specific service requirements prior to service execution.'])}
                  className="px-3 py-1 bg-white border border-slate-300 hover:border-amber-500 text-amber-800 rounded-xl text-xs font-bold transition-colors"
                >
                  + Add Note
                </button>
              </div>
            ) : (
              importantNotes.map((noteText, idx) => (
                <div key={idx} className="p-5 bg-amber-50/40 rounded-3xl border border-amber-200 space-y-3 shadow-xs">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2 flex-1">
                      <AlertTriangle className="w-5 h-5 text-amber-500 ml-1 flex-shrink-0" />
                      <input
                        type="text"
                        value={noteText}
                        onChange={(e) => {
                          const copy = [...importantNotes];
                          copy[idx] = e.target.value;
                          setImportantNotes(copy);
                        }}
                        placeholder="Describe important service-specific disclosure..."
                        className="w-full bg-white border border-amber-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500/30"
                        required
                      />
                    </div>
                    <div className="flex items-center gap-1 flex-shrink-0">
                      <button
                        type="button"
                        disabled={idx === 0}
                        onClick={() => {
                          const copy = [...importantNotes];
                          const temp = copy[idx - 1];
                          copy[idx - 1] = copy[idx];
                          copy[idx] = temp;
                          setImportantNotes(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Up"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        disabled={idx === importantNotes.length - 1}
                        onClick={() => {
                          const copy = [...importantNotes];
                          const temp = copy[idx + 1];
                          copy[idx + 1] = copy[idx];
                          copy[idx] = temp;
                          setImportantNotes(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Down"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setImportantNotes(importantNotes.filter((_, i) => i !== idx))}
                        className="p-1 text-rose-400 hover:text-rose-600"
                        title="Delete Note"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 11: Service Warranty & Guarantee */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <ShieldCheck className="w-6 h-6 text-slate-700" />
                <span>11. Service Warranty & Guarantee</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Formal warranty coverage terms and service guarantee policy</p>
            </div>
            {warranty && warranty.trim() !== '' ? (
              <button
                type="button"
                onClick={() => setWarranty(null)}
                className="px-3 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
              >
                Remove Warranty
              </button>
            ) : (
              <button
                type="button"
                onClick={() => setWarranty('30-Day Workmanship Coverage: Re-inspection and correction provided for applicable service defects.')}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-300 rounded-xl text-xs md:text-sm font-bold transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Add Warranty</span>
              </button>
            )}
          </div>

          {!warranty || warranty.trim() === '' ? (
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-sm">
              <span className="text-slate-500 font-semibold flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-slate-400" />
                No warranty or guarantee specified for this service.
              </span>
              <button
                type="button"
                onClick={() => setWarranty('30-Day Workmanship Coverage: Re-inspection and correction provided for applicable service defects.')}
                className="px-3 py-1 bg-white border border-slate-300 hover:border-slate-500 text-slate-800 rounded-xl text-xs font-bold transition-colors"
              >
                + Add Warranty
              </button>
            </div>
          ) : (
            <div className="p-6 bg-slate-50/70 rounded-3xl border border-slate-200 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-bold text-slate-700">Warranty Coverage Terms & Conditions</label>
                <textarea
                  value={warranty}
                  onChange={(e) => setWarranty(e.target.value)}
                  placeholder="Describe warranty duration, terms, exclusions, and conditions..."
                  className="w-full bg-white border border-slate-200 rounded-2xl p-4 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400/30"
                  rows={3}
                  required
                />
              </div>
            </div>
          )}
        </div>

        {/* Section 12: Frequently Asked Questions (FAQs) */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <HelpCircle className="w-6 h-6 text-amber-500" />
                <span>12. Customer FAQs ({faqs.length})</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Realistic questions and clear answers specifically for this service</p>
            </div>
            <button
              type="button"
              onClick={() => setFaqs([...faqs, { question: 'What does this service include?', answer: 'Provides complete service execution according to specifications.' }])}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add FAQ</span>
            </button>
          </div>

          <div className="space-y-4">
            {faqs.length === 0 ? (
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-sm">
                <span className="text-slate-500 font-semibold flex items-center gap-2">
                  <HelpCircle className="w-4 h-4 text-amber-500" />
                  No FAQs configured for this service.
                </span>
                <button
                  type="button"
                  onClick={() => setFaqs([{ question: `What is included in ${name}?`, answer: `Service includes standard ${category} execution.` }])}
                  className="px-3 py-1 bg-white border border-slate-300 hover:border-amber-500 text-amber-800 rounded-xl text-xs font-bold transition-colors"
                >
                  + Add FAQ
                </button>
              </div>
            ) : (
              faqs.map((faq, idx) => (
                <div key={idx} className="p-5 bg-amber-50/30 rounded-3xl border border-amber-200 space-y-3 shadow-xs">
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-sm font-bold text-amber-900 flex items-center gap-1.5">
                      <HelpCircle className="w-4 h-4 text-amber-600" />
                      Question #{idx + 1}
                    </span>
                    <div className="flex items-center gap-1">
                      <button
                        type="button"
                        disabled={idx === 0}
                        onClick={() => {
                          const copy = [...faqs];
                          const temp = copy[idx - 1];
                          copy[idx - 1] = copy[idx];
                          copy[idx] = temp;
                          setFaqs(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Up"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        disabled={idx === faqs.length - 1}
                        onClick={() => {
                          const copy = [...faqs];
                          const temp = copy[idx + 1];
                          copy[idx + 1] = copy[idx];
                          copy[idx] = temp;
                          setFaqs(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Down"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setFaqs(faqs.filter((_, i) => i !== idx))}
                        className="p-1 text-rose-400 hover:text-rose-600"
                        title="Delete FAQ"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <input
                    type="text"
                    value={faq.question}
                    onChange={(e) => {
                      const copy = [...faqs];
                      copy[idx].question = e.target.value;
                      setFaqs(copy);
                    }}
                    placeholder="Enter question..."
                    className="w-full bg-white border border-amber-200 rounded-xl px-4 py-2.5 text-base font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500/30"
                    required
                  />
                  <textarea
                    value={faq.answer}
                    onChange={(e) => {
                      const copy = [...faqs];
                      copy[idx].answer = e.target.value;
                      setFaqs(copy);
                    }}
                    placeholder="Enter clear answer..."
                    className="w-full bg-white border border-amber-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-amber-500/30"
                    rows={2}
                    required
                  />
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 13: SEO & Service Metadata */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <Sparkles className="w-6 h-6 text-[#5CA8FF]" />
                <span>13. SEO & Service Metadata</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Search engine title, meta description, keywords, and service highlights</p>
            </div>
            <button
              type="button"
              onClick={() => setConfirmRegenerateOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 hover:bg-blue-100 text-[#5CA8FF] border border-blue-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Sparkles className="w-4 h-4 text-[#5CA8FF]" />
              <span>Generate / Regenerate Metadata</span>
            </button>
          </div>

          {!seoTitle && !seoDescription && keywords.length === 0 ? (
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-sm">
              <span className="text-slate-500 font-semibold flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#5CA8FF]" />
                No SEO metadata configured.
              </span>
              <button
                type="button"
                onClick={() => {
                  setSeoTitle(`${name} | Professional ${category} Service`);
                  setSeoDescription(`Book professional ${name.toLowerCase()} services online with top-rated experts.`);
                  setKeywords([name.toLowerCase(), category.toLowerCase(), subcategory.toLowerCase()]);
                }}
                className="px-3 py-1 bg-white border border-slate-300 hover:border-[#5CA8FF] text-[#5CA8FF] rounded-xl text-xs font-bold transition-colors"
              >
                + Configure Metadata
              </button>
            </div>
          ) : (
            <div className="space-y-5 text-base">
              {/* SEO Title */}
              <div className="space-y-2">
                <label className="text-sm md:text-base font-bold text-slate-800">SEO Page Title</label>
                <input
                  type="text"
                  value={seoTitle}
                  onChange={(e) => setSeoTitle(e.target.value)}
                  placeholder="e.g. Pedicure at Home | Professional Foot & Nail Care"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                />
              </div>

              {/* SEO Description */}
              <div className="space-y-2">
                <label className="text-sm md:text-base font-bold text-slate-800">SEO Meta Description</label>
                <textarea
                  value={seoDescription}
                  onChange={(e) => setSeoDescription(e.target.value)}
                  placeholder="e.g. Book professional pedicure services at home with hygienic tools..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                  rows={2}
                />
              </div>

              {/* Short Service Summary */}
              <div className="space-y-2">
                <label className="text-sm md:text-base font-bold text-slate-800">Short Service Summary</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Brief service description..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                  rows={2}
                />
              </div>

              {/* Search Keywords (Chips) */}
              <div className="space-y-3">
                <label className="text-sm md:text-base font-bold text-slate-800 flex items-center justify-between">
                  <span>Search Keywords ({keywords.length})</span>
                </label>

                <div className="flex flex-wrap items-center gap-2 bg-slate-50 p-4 rounded-2xl border border-slate-200">
                  {keywords.map((kw, i) => (
                    <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1 bg-white border border-slate-200 rounded-xl text-sm font-semibold text-slate-800 shadow-xs">
                      {kw}
                      <button
                        type="button"
                        onClick={() => setKeywords(keywords.filter((_, idx) => idx !== i))}
                        className="text-slate-400 hover:text-rose-600 font-bold ml-1"
                        title="Remove Keyword"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                  <div className="flex items-center gap-2 mt-1 w-full sm:w-auto">
                    <input
                      type="text"
                      value={newKeywordInput}
                      onChange={(e) => setNewKeywordInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          if (newKeywordInput.trim() && !keywords.includes(newKeywordInput.trim())) {
                            setKeywords([...keywords, newKeywordInput.trim()]);
                            setNewKeywordInput('');
                          }
                        }
                      }}
                      placeholder="Add search keyword..."
                      className="bg-white border border-slate-200 rounded-xl px-3 py-1 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                    />
                    <button
                      type="button"
                      onClick={() => {
                        if (newKeywordInput.trim() && !keywords.includes(newKeywordInput.trim())) {
                          setKeywords([...keywords, newKeywordInput.trim()]);
                          setNewKeywordInput('');
                        }
                      }}
                      className="px-3 py-1 bg-[#5CA8FF] hover:bg-[#4A96ED] text-white rounded-xl text-xs font-bold transition-colors"
                    >
                      + Add Keyword
                    </button>
                  </div>
                </div>
              </div>

              {/* Service Highlights (Chips) */}
              <div className="space-y-3">
                <label className="text-sm md:text-base font-bold text-slate-800 flex items-center justify-between">
                  <span>Service Highlights ({highlights.length})</span>
                </label>

                <div className="flex flex-wrap items-center gap-2 bg-blue-50/40 p-4 rounded-2xl border border-blue-100">
                  {highlights.map((hl, i) => (
                    <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1 bg-white border border-blue-200 rounded-xl text-sm font-semibold text-slate-900 shadow-xs">
                      <Sparkles className="w-3.5 h-3.5 text-[#5CA8FF]" />
                      {hl}
                      <button
                        type="button"
                        onClick={() => setHighlights(highlights.filter((_, idx) => idx !== i))}
                        className="text-slate-400 hover:text-rose-600 font-bold ml-1"
                        title="Remove Highlight"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                  <div className="flex items-center gap-2 mt-1 w-full sm:w-auto">
                    <input
                      type="text"
                      value={newHighlightInput}
                      onChange={(e) => setNewHighlightInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          if (newHighlightInput.trim() && !highlights.includes(newHighlightInput.trim())) {
                            setHighlights([...highlights, newHighlightInput.trim()]);
                            setNewHighlightInput('');
                          }
                        }
                      }}
                      placeholder="Add highlight..."
                      className="bg-white border border-slate-200 rounded-xl px-3 py-1 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                    />
                    <button
                      type="button"
                      onClick={() => {
                        if (newHighlightInput.trim() && !highlights.includes(newHighlightInput.trim())) {
                          setHighlights([...highlights, newHighlightInput.trim()]);
                          setNewHighlightInput('');
                        }
                      }}
                      className="px-3 py-1 bg-[#5CA8FF] hover:bg-[#4A96ED] text-white rounded-xl text-xs font-bold transition-colors"
                    >
                      + Add Highlight
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Section 14: Service Features & Highlights */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <CheckCircle2 className="w-6 h-6 text-[#5CA8FF]" />
                <span>14. Key Service Features & Specifications</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Meaningful service-specific features and technical capabilities ({serviceFeatures.length} Features)</p>
            </div>
            <button
              type="button"
              onClick={() => setServiceFeatures([...serviceFeatures, { title: 'New Service Feature', description: 'Feature description...' }])}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-[#5CA8FF] border border-blue-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Feature</span>
            </button>
          </div>

          <div className="space-y-4">
            {serviceFeatures.length === 0 ? (
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-sm">
                <span className="text-slate-500 font-semibold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#5CA8FF]" />
                  No service features added.
                </span>
                <button
                  type="button"
                  onClick={() => setServiceFeatures([{ title: 'Core Service Execution', description: 'Performed according to standard service specifications.' }])}
                  className="px-3 py-1 bg-white border border-slate-300 hover:border-[#5CA8FF] text-[#5CA8FF] rounded-xl text-xs font-bold transition-colors"
                >
                  + Add Feature
                </button>
              </div>
            ) : (
              serviceFeatures.map((feat, idx) => (
                <div key={idx} className="p-5 bg-blue-50/30 rounded-3xl border border-blue-100 space-y-3 shadow-xs">
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#5CA8FF]" />
                      Feature #{idx + 1}
                    </span>
                    <div className="flex items-center gap-1">
                      <button
                        type="button"
                        disabled={idx === 0}
                        onClick={() => {
                          const copy = [...serviceFeatures];
                          const temp = copy[idx - 1];
                          copy[idx - 1] = copy[idx];
                          copy[idx] = temp;
                          setServiceFeatures(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Up"
                      >
                        <ArrowUp className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        disabled={idx === serviceFeatures.length - 1}
                        onClick={() => {
                          const copy = [...serviceFeatures];
                          const temp = copy[idx + 1];
                          copy[idx + 1] = copy[idx];
                          copy[idx] = temp;
                          setServiceFeatures(copy);
                        }}
                        className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-30"
                        title="Move Down"
                      >
                        <ArrowDown className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setServiceFeatures(serviceFeatures.filter((_, i) => i !== idx))}
                        className="p-1 text-rose-400 hover:text-rose-600"
                        title="Delete Feature"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <input
                    type="text"
                    value={feat.title}
                    onChange={(e) => {
                      const copy = [...serviceFeatures];
                      copy[idx].title = e.target.value;
                      setServiceFeatures(copy);
                    }}
                    placeholder="Feature title..."
                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-base font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                    required
                  />
                  <input
                    type="text"
                    value={feat.description}
                    onChange={(e) => {
                      const copy = [...serviceFeatures];
                      copy[idx].description = e.target.value;
                      setServiceFeatures(copy);
                    }}
                    placeholder="Feature description (optional)..."
                    className="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                  />
                </div>
              ))
            )}
          </div>
        </div>

        {/* Section 15: Service Status & Booking Availability */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <ShieldCheck className="w-6 h-6 text-slate-700" />
                <span>15. Service Status & Booking Availability</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Control customer booking availability for this catalog item</p>
            </div>
            {isActive ? (
              <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-sm font-bold">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                ● Active
              </span>
            ) : (
              <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200 text-sm font-bold">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
                ● Inactive
              </span>
            )}
          </div>

          <div className="p-6 bg-slate-50/70 rounded-3xl border border-slate-200 space-y-5">
            <div className="space-y-3">
              <label className="text-sm md:text-base font-bold text-slate-800">Booking Availability Status</label>
              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  type="button"
                  onClick={() => setIsActive(true)}
                  className={`flex-1 flex items-center justify-between p-4 rounded-2xl border transition-all ${
                    isActive
                      ? 'bg-white border-emerald-500 ring-2 ring-emerald-500/20 text-emerald-900 shadow-sm'
                      : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <CheckCircle2 className={`w-5 h-5 ${isActive ? 'text-emerald-600' : 'text-slate-400'}`} />
                    <div className="text-left">
                      <p className="font-bold text-base">ACTIVE</p>
                      <p className="text-xs text-slate-500 font-medium">Service is available for customer bookings</p>
                    </div>
                  </div>
                  {isActive && <Check className="w-5 h-5 text-emerald-600 font-bold" />}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    if (isActive) {
                      setDeactivateModalOpen(true);
                    } else {
                      setIsActive(false);
                    }
                  }}
                  className={`flex-1 flex items-center justify-between p-4 rounded-2xl border transition-all ${
                    !isActive
                      ? 'bg-white border-rose-500 ring-2 ring-rose-500/20 text-rose-900 shadow-sm'
                      : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <XCircle className={`w-5 h-5 ${!isActive ? 'text-rose-600' : 'text-slate-400'}`} />
                    <div className="text-left">
                      <p className="font-bold text-base">INACTIVE</p>
                      <p className="text-xs text-slate-500 font-medium">Service disabled for new bookings</p>
                    </div>
                  </div>
                  {!isActive && <X className="w-5 h-5 text-rose-600 font-bold" />}
                </button>
              </div>
            </div>

            {!isActive && (
              <div className="space-y-2">
                <label className="text-sm font-bold text-slate-700">Reason for Temporary Unavailability (Optional)</label>
                <input
                  type="text"
                  value={unavailabilityReason}
                  onChange={(e) => setUnavailabilityReason(e.target.value)}
                  placeholder="e.g. Seasonal downtime, technician training, material shortage..."
                  className="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-base font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-rose-500/20"
                />
              </div>
            )}
          </div>
        </div>

        {/* Section 16: Service Media & Visual Gallery */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <ImageIcon className="w-6 h-6 text-[#5CA8FF]" />
                <span>16. Service Media & Visual Gallery</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">Manage cover photo and gallery media associated with this exact service ({serviceMedia.length} Media Items)</p>
            </div>
            <button
              type="button"
              onClick={() => {
                const newId = `media_${Date.now()}`;
                const newCover = serviceMedia.length === 0;
                setServiceMedia([
                  ...serviceMedia,
                  { id: newId, url: 'https://images.unsplash.com/photo-1540555700478-4be289fbecef', caption: `${name} service image`, media_type: 'gallery', is_cover: newCover }
                ]);
              }}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-[#5CA8FF] border border-blue-200 rounded-xl text-xs md:text-sm font-bold transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Image</span>
            </button>
          </div>

          {serviceMedia.length === 0 ? (
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-sm">
              <span className="text-slate-500 font-semibold flex items-center gap-2">
                <ImageIcon className="w-4 h-4 text-slate-400" />
                No service images added.
              </span>
              <button
                type="button"
                onClick={() => {
                  setServiceMedia([
                    { id: `media_${Date.now()}`, url: 'https://images.unsplash.com/photo-1540555700478-4be289fbecef', caption: `${name} cover photo`, media_type: 'gallery', is_cover: true }
                  ]);
                }}
                className="px-3 py-1 bg-white border border-slate-300 hover:border-[#5CA8FF] text-[#5CA8FF] rounded-xl text-xs font-bold transition-colors"
              >
                + Add Image
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {serviceMedia.map((m, idx) => (
                <div key={m.id || idx} className="bg-slate-50 border border-slate-200 rounded-2xl p-3 space-y-3 relative group">
                  <div className="relative h-36 w-full rounded-xl overflow-hidden bg-slate-200 border border-slate-200">
                    <img src={m.url} alt={m.caption || name} className="h-full w-full object-cover" />
                    {m.is_cover && (
                      <span className="absolute top-2 left-2 px-2.5 py-0.5 bg-amber-500 text-white rounded-lg text-xs font-bold shadow-xs">
                        Cover Photo
                      </span>
                    )}
                  </div>

                  <div className="space-y-2">
                    <input
                      type="text"
                      value={m.caption}
                      onChange={(e) => {
                        const copy = [...serviceMedia];
                        copy[idx].caption = e.target.value;
                        setServiceMedia(copy);
                      }}
                      placeholder="Image caption..."
                      className="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/30"
                    />

                    <div className="flex items-center justify-between gap-1 text-xs">
                      <select
                        value={m.media_type}
                        onChange={(e) => {
                          const copy = [...serviceMedia];
                          copy[idx].media_type = e.target.value;
                          setServiceMedia(copy);
                        }}
                        className="bg-white border border-slate-200 rounded-lg px-2 py-1 font-semibold text-slate-700 focus:outline-none text-xs"
                      >
                        <option value="gallery">Gallery</option>
                        <option value="process">Process</option>
                        <option value="before_after">Before / After</option>
                      </select>

                      <div className="flex items-center gap-1">
                        <button
                          type="button"
                          onClick={() => {
                            const copy = serviceMedia.map((item, i) => ({
                              ...item,
                              is_cover: i === idx
                            }));
                            setServiceMedia(copy);
                          }}
                          className={`p-1 rounded-lg border text-xs font-bold transition-colors ${
                            m.is_cover ? 'bg-amber-50 text-amber-600 border-amber-200' : 'bg-white text-slate-400 border-slate-200 hover:text-slate-700'
                          }`}
                          title="Set as Cover Photo"
                        >
                          Cover
                        </button>

                        <button
                          type="button"
                          onClick={() => setServiceMedia(serviceMedia.filter((_, i) => i !== idx))}
                          className="p-1 text-rose-400 hover:text-rose-600"
                          title="Delete Media"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Section 17: Activity & Change History */}
        <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-slate-900 flex items-center gap-2">
                <History className="w-6 h-6 text-[#5CA8FF]" />
                <span>17. Activity & Change History</span>
              </h2>
              <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
                Immutable administrative audit trail for this exact service ({auditLogs.length} Audit Entries)
              </p>
            </div>

            <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-2xl border border-slate-200">
              {['all', 'pricing', 'status', 'content'].map((filterKey) => (
                <button
                  key={filterKey}
                  type="button"
                  onClick={() => setAuditFilter(filterKey)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold capitalize transition-colors ${
                    auditFilter === filterKey
                      ? 'bg-white text-slate-900 shadow-xs'
                      : 'text-slate-500 hover:text-slate-800'
                  }`}
                >
                  {filterKey}
                </button>
              ))}
            </div>
          </div>

          {auditLoading ? (
            <div className="p-8 text-center space-y-2">
              <Loader2 className="w-6 h-6 animate-spin text-[#5CA8FF] mx-auto" />
              <p className="text-sm font-semibold text-slate-500">Loading audit history ledger...</p>
            </div>
          ) : auditLogs.length === 0 ? (
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-sm">
              <span className="text-slate-500 font-semibold flex items-center gap-2">
                <History className="w-4 h-4 text-slate-400" />
                No recorded activity for this service.
              </span>
              <span className="text-xs text-slate-400 font-semibold italic">Immutable Audit Record</span>
            </div>
          ) : (
            <div className="space-y-4">
              {auditLogs
                .filter((log) => {
                  if (auditFilter === 'pricing') return log.action.toLowerCase().includes('price');
                  if (auditFilter === 'status') return log.action.toLowerCase().includes('status') || log.action.toLowerCase().includes('active');
                  if (auditFilter === 'content') return !log.action.toLowerCase().includes('price') && !log.action.toLowerCase().includes('status');
                  return true;
                })
                .map((log) => (
                  <div key={log.id} className="p-5 bg-slate-50 rounded-2xl border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-2">
                        <span className="text-base font-bold text-slate-900">{log.action}</span>
                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${
                          log.risk_level === 'Critical'
                            ? 'bg-rose-50 text-rose-700 border-rose-200'
                            : log.risk_level === 'Warning'
                            ? 'bg-amber-50 text-amber-700 border-amber-200'
                            : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                        }`}>
                          {log.risk_level}
                        </span>
                      </div>

                      {log.metadata_json?.changes_summary && (
                        <p className="text-sm font-semibold text-slate-700 bg-white px-3 py-1.5 rounded-xl border border-slate-200 font-mono">
                          {log.metadata_json.changes_summary}
                        </p>
                      )}

                      <p className="text-xs text-slate-500 font-semibold flex items-center gap-2 pt-0.5">
                        <span>Admin: <strong className="text-slate-800">{log.actor_email}</strong> ({log.actor_role})</span>
                        {log.ip_address && <span>• IP: {log.ip_address}</span>}
                      </p>
                    </div>

                    <div className="text-right flex-shrink-0">
                      <span className="text-xs font-bold text-slate-400 block">
                        {new Date(log.created_at).toLocaleDateString('en-IN', {
                          day: '2-digit',
                          month: 'short',
                          year: 'numeric'
                        })}
                      </span>
                      <span className="text-xs font-semibold text-slate-500">
                        {new Date(log.created_at).toLocaleTimeString('en-IN', {
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </span>
                    </div>
                  </div>
                ))}

              <div className="p-3 bg-slate-100/60 rounded-xl text-center text-xs text-slate-500 font-semibold italic">
                🔒 Audit history is read-only and immutably stored in SmartServe security ledger.
              </div>
            </div>
          )}
        </div>

      </form>

      {/* Confirmation Modal Before Deactivating Service */}
      {deactivateModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-slate-200 overflow-hidden animate-in fade-in p-6 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center mx-auto">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div className="text-center space-y-2">
              <h3 className="text-lg font-bold text-slate-900">Deactivate {name}?</h3>
              <p className="text-sm text-slate-600 font-medium">
                Are you sure you want to deactivate this service? Customers will no longer be able to book it.
              </p>
            </div>
            <div className="flex items-center gap-3 pt-2">
              <button
                type="button"
                onClick={() => setDeactivateModalOpen(false)}
                className="flex-1 py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-sm font-bold transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsActive(false);
                  setDeactivateModalOpen(false);
                }}
                className="flex-1 py-2.5 px-4 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-sm font-bold shadow-xs transition-colors"
              >
                Confirm Deactivation
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Modal Before Regeneration */}
      {confirmRegenerateOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-slate-200 overflow-hidden animate-in fade-in p-6 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mx-auto">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div className="text-center space-y-2">
              <h3 className="text-lg font-bold text-slate-900">Confirm AI Regeneration</h3>
              <p className="text-sm text-slate-600 font-medium">
                This will generate fresh AI content for <strong>{name}</strong> using OpenRouter LLM. Manually edited content may be overwritten upon review.
              </p>
            </div>
            <div className="flex items-center justify-end gap-3 pt-3">
              <button
                onClick={() => setConfirmRegenerateOpen(false)}
                className="px-5 py-2.5 bg-slate-100 text-slate-700 font-bold rounded-2xl text-xs"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmRegenerate}
                className="px-5 py-2.5 bg-[#5CA8FF] hover:bg-blue-600 text-white font-bold rounded-2xl text-xs shadow-sm"
              >
                Proceed to Regenerate
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Validated AI Output Review Modal */}
      {aiReviewOpen && aiGeneratedData && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[85vh] animate-in fade-in">
            <div className="flex items-center justify-between px-8 py-5 border-b border-slate-100 bg-blue-50">
              <div className="flex items-center gap-3">
                <Sparkles className="w-6 h-6 text-[#5CA8FF]" />
                <h3 className="font-bold text-slate-900 text-base">Review Validated AI Output</h3>
              </div>
              <button onClick={() => setAiReviewOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="p-8 overflow-y-auto space-y-5 text-sm">
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                <p className="font-bold text-slate-900">AI Description:</p>
                <p className="text-slate-700 mt-1 font-medium">{aiGeneratedData.description}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-100">
                  <p className="font-bold text-emerald-800">Validated Inclusions ({aiGeneratedData.included?.length || 0}):</p>
                  <ul className="list-disc list-inside text-slate-700 mt-2 space-y-1 font-medium">
                    {aiGeneratedData.included?.map((item: string, i: number) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="bg-rose-50/50 p-4 rounded-2xl border border-rose-100">
                  <p className="font-bold text-rose-800">Validated Exclusions ({aiGeneratedData.excluded?.length || 0}):</p>
                  <ul className="list-disc list-inside text-slate-700 mt-2 space-y-1 font-medium">
                    {aiGeneratedData.excluded?.map((item: string, i: number) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div>
                <p className="font-bold text-slate-900">Process Steps ({(aiGeneratedData.process_steps || aiGeneratedData.how_it_works || []).length}):</p>
                <ol className="list-decimal list-inside text-slate-700 mt-2 space-y-1.5 font-medium">
                  {(aiGeneratedData.process_steps || aiGeneratedData.how_it_works || []).map((step: any, i: number) => (
                    <li key={i}><span className="font-bold text-slate-900">{step.title}</span> — {step.description}</li>
                  ))}
                </ol>
              </div>

              <div className="pt-2 text-xs text-slate-400 italic">
                Deterministic validator filtered domain mismatches. Click "Apply to Form" to replace editor fields.
              </div>
            </div>

            <div className="p-5 border-t border-slate-100 bg-slate-50 flex items-center justify-end gap-4">
              <button
                onClick={() => setAiReviewOpen(false)}
                className="px-5 py-2.5 bg-slate-200 text-slate-700 font-bold rounded-2xl text-xs"
              >
                Discard
              </button>
              <button
                onClick={handleApplyAiData}
                className="px-6 py-2.5 bg-[#5CA8FF] text-white font-bold rounded-2xl text-xs shadow-sm hover:bg-blue-600"
              >
                Apply to Form
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Customer-Facing Service Preview Modal */}
      {previewModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
          <div className="bg-white w-full max-w-4xl max-h-[92vh] rounded-3xl shadow-2xl border border-slate-200 overflow-y-auto animate-in fade-in space-y-0">
            {/* Customer Header Banner */}
            <div className="sticky top-0 z-20 bg-white/95 backdrop-blur-sm p-6 border-b border-slate-100 flex items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <span>{category}</span>
                  <span>•</span>
                  <span>{subcategory}</span>
                </div>
                <h1 className="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">{name}</h1>
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => setIsActive(!isActive)}
                  className={`px-4 py-2 rounded-xl text-xs md:text-sm font-bold border transition-colors ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100'
                      : 'bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100'
                  }`}
                >
                  {isActive ? '● Active (Publish)' : '● Inactive (Unpublished)'}
                </button>

                <button
                  type="button"
                  onClick={() => setPreviewModalOpen(false)}
                  className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold transition-colors"
                  title="Close Preview"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Status Banner */}
            <div className={`px-6 py-3 text-xs md:text-sm font-bold flex items-center gap-2 ${
              isActive ? 'bg-emerald-50 text-emerald-800 border-b border-emerald-100' : 'bg-rose-50 text-rose-800 border-b border-rose-100'
            }`}>
              {isActive ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>This service is currently available for customer bookings.</span>
                </>
              ) : (
                <>
                  <XCircle className="w-4 h-4 text-rose-600" />
                  <span>Customers cannot currently book this service.</span>
                </>
              )}
            </div>

            {/* Pre-Publish Quality Audit Bar */}
            <div className="p-6 bg-slate-50 border-b border-slate-100 space-y-2">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">Pre-Publish Completeness Check</p>
              <div className="flex flex-wrap items-center gap-3 text-xs font-semibold">
                <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">✓ Name</span>
                <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">✓ Category</span>
                <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">✓ Price ({formatRupee(basePrice)})</span>
                {description ? (
                  <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">✓ Description</span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">⚠ Description Missing</span>
                )}
                {included.length > 0 ? (
                  <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">✓ Scope Defined</span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">⚠ Scope Undefined</span>
                )}
                {serviceMedia.length === 0 && (
                  <span className="inline-flex items-center gap-1 text-slate-600 bg-slate-100 px-2.5 py-1 rounded-lg border border-slate-200">ℹ No Cover Media</span>
                )}
              </div>
            </div>

            {/* Customer Body Content */}
            <div className="p-6 md:p-8 space-y-8">
              {/* Media Header if Cover Photo Exists */}
              {serviceMedia.length > 0 && (
                <div className="h-56 md:h-72 w-full rounded-2xl overflow-hidden bg-slate-100 border border-slate-200 relative">
                  <img
                    src={(serviceMedia.find(m => m.is_cover) || serviceMedia[0]).url}
                    alt={name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute bottom-3 left-3 bg-slate-900/70 backdrop-blur-sm text-white px-3 py-1 rounded-xl text-xs font-semibold">
                    {(serviceMedia.find(m => m.is_cover) || serviceMedia[0]).caption || name}
                  </div>
                </div>
              )}

              {/* Price & Overview Card */}
              <div className="p-6 bg-blue-50/40 rounded-2xl border border-blue-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="space-y-1">
                  <p className="text-xs font-bold text-slate-500 uppercase">Service Price</p>
                  <p className="text-3xl font-extrabold text-slate-900 font-mono">{formatRupee(basePrice)}</p>
                </div>
                {estimatedDuration > 0 && (
                  <div className="space-y-1 sm:text-right">
                    <p className="text-xs font-bold text-slate-500 uppercase">Estimated Duration</p>
                    <p className="text-lg font-bold text-slate-800 flex items-center sm:justify-end gap-1.5">
                      <Clock className="w-5 h-5 text-[#5CA8FF]" />
                      {estimatedDuration} Minutes
                    </p>
                  </div>
                )}
              </div>

              {/* Description & Highlights */}
              <div className="space-y-3">
                <h2 className="text-xl font-bold text-slate-900">About This Service</h2>
                <p className="text-base text-slate-700 font-medium leading-relaxed">{description || 'No description provided.'}</p>
                {highlights.length > 0 && (
                  <div className="flex flex-wrap gap-2 pt-2">
                    {highlights.map((hl, i) => (
                      <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-blue-50 text-[#5CA8FF] border border-blue-200 rounded-xl text-xs font-bold">
                        <Sparkles className="w-3.5 h-3.5" />
                        {hl}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Scope: Included vs Excluded (Rendered only if data exists!) */}
              {(included.length > 0 || excluded.length > 0) && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {included.length > 0 && (
                    <div className="p-6 bg-emerald-50/40 rounded-2xl border border-emerald-100 space-y-3">
                      <h3 className="text-lg font-bold text-emerald-950 flex items-center gap-2">
                        <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                        What's Included
                      </h3>
                      <ul className="space-y-2 text-sm font-semibold text-slate-800">
                        {included.map((item, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-emerald-600 font-bold">•</span>
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {excluded.length > 0 && (
                    <div className="p-6 bg-rose-50/40 rounded-2xl border border-rose-100 space-y-3">
                      <h3 className="text-lg font-bold text-rose-950 flex items-center gap-2">
                        <XCircle className="w-5 h-5 text-rose-600" />
                        What's Excluded
                      </h3>
                      <ul className="space-y-2 text-sm font-semibold text-slate-800">
                        {excluded.map((item, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-rose-600 font-bold">•</span>
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* How It Works / Process Steps (Rendered only if data exists!) */}
              {processSteps.length > 0 && (
                <div className="space-y-4">
                  <h2 className="text-xl font-bold text-slate-900">How It Works</h2>
                  <div className="space-y-3">
                    {processSteps.map((step, i) => (
                      <div key={i} className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-start gap-4">
                        <div className="w-8 h-8 rounded-xl bg-[#5CA8FF] text-white flex items-center justify-center font-bold text-sm flex-shrink-0">
                          {step.step_number || i + 1}
                        </div>
                        <div className="space-y-1">
                          <p className="font-bold text-slate-900 text-base">{step.title}</p>
                          <p className="text-sm text-slate-600 font-medium">{step.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tools & Materials (Rendered only if data exists!) */}
              {toolsMaterials.length > 0 && (
                <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
                  <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                    <Wrench className="w-5 h-5 text-slate-700" />
                    Tools & Equipment
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {toolsMaterials.map((t, i) => (
                      <span key={i} className="px-3 py-1 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 shadow-xs">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Customer Preparation (Rendered ONLY if data exists! Hides for Pedicure!) */}
              {customerSetup.length > 0 && (
                <div className="p-6 bg-blue-50/30 rounded-2xl border border-blue-100 space-y-3">
                  <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                    <Layers className="w-5 h-5 text-[#5CA8FF]" />
                    Customer Preparation
                  </h3>
                  <ul className="space-y-2 text-sm font-semibold text-slate-800">
                    {customerSetup.map((item, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-[#5CA8FF] font-bold">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Aftercare & Precautions (Rendered only if data exists!) */}
              {aftercare.length > 0 && (
                <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
                  <h3 className="text-lg font-bold text-slate-900">Aftercare & Maintenance</h3>
                  <ul className="space-y-2 text-sm font-semibold text-slate-800">
                    {aftercare.map((item, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-slate-600 font-bold">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Expected Results (Rendered only if data exists!) */}
              {expectedResults.length > 0 && (
                <div className="p-6 bg-emerald-50/30 rounded-2xl border border-emerald-100 space-y-3">
                  <h3 className="text-lg font-bold text-emerald-950">Expected Results</h3>
                  <ul className="space-y-2 text-sm font-semibold text-slate-800">
                    {expectedResults.map((item, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-emerald-600 font-bold">✓</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Frequently Asked Questions (Rendered only if data exists!) */}
              {faqs.length > 0 && (
                <div className="space-y-4">
                  <h2 className="text-xl font-bold text-slate-900">Frequently Asked Questions</h2>
                  <div className="space-y-3">
                    {faqs.map((f, i) => (
                      <div key={i} className="p-5 bg-amber-50/30 rounded-2xl border border-amber-200 space-y-2">
                        <p className="font-bold text-slate-900 text-base">Q: {f.question}</p>
                        <p className="text-sm text-slate-700 font-medium">A: {f.answer}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Warranty Coverage (Rendered ONLY if warranty exists and is non-empty! Hides for Pedicure!) */}
              {warranty && warranty.trim() !== '' && (
                <div className="p-6 bg-slate-900 text-white rounded-2xl space-y-2">
                  <h3 className="text-lg font-bold flex items-center gap-2">
                    <ShieldCheck className="w-5 h-5 text-emerald-400" />
                    Service Warranty & Guarantee
                  </h3>
                  <p className="text-sm font-medium text-slate-300">{warranty}</p>
                </div>
              )}
            </div>

            {/* Modal Footer Actions */}
            <div className="p-6 border-t border-slate-100 bg-slate-50 flex items-center justify-between gap-4">
              <button
                type="button"
                onClick={() => setPreviewModalOpen(false)}
                className="px-5 py-2.5 bg-slate-200 text-slate-700 font-bold rounded-2xl text-xs md:text-sm"
              >
                Close Preview
              </button>

              <button
                type="button"
                onClick={() => {
                  setIsActive(!isActive);
                  setPreviewModalOpen(false);
                  setSaveToast(isActive ? 'Service unpublished (Deactivated).' : 'Service published (Activated)!');
                  setTimeout(() => setSaveToast(null), 4000);
                }}
                className={`px-6 py-2.5 font-bold rounded-2xl text-xs md:text-sm shadow-sm transition-colors ${
                  isActive
                    ? 'bg-rose-600 hover:bg-rose-700 text-white'
                    : 'bg-emerald-600 hover:bg-emerald-700 text-white'
                }`}
              >
                {isActive ? 'Deactivate Service' : 'Publish Service Now'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
