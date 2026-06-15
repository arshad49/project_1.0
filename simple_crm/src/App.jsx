import { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Users,
  KanbanSquare,
  History,
  CalendarClock,
  Plus,
  Search,
  Filter,
  Eye,
  Pencil,
  Trash2,
  X,
  Menu,
  TrendingUp,
  Briefcase,
  Check,
  CheckCircle,
  AlertTriangle,
  Info,
  Settings,
  Clock,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

const MOCK_LEADS = [
  { id: "1716462000000", name: "Bruce Wayne", company: "Wayne Enterprises", email: "bruce@waynecorp.com", phone: "555-0199", source: "Referral", status: "Qualified", created_at: "2026-05-20T09:30:00.000Z", value: "125000" },
  { id: "1716463200000", name: "Tony Stark", company: "Stark Industries", email: "tony@stark.com", phone: "555-3000", source: "LinkedIn", status: "Proposal", created_at: "2026-05-21T10:15:00.000Z", value: "250000" },
  { id: "1716464400000", name: "Lex Luthor", company: "LexCorp", email: "lex@lexcorp.com", phone: "555-4040", source: "Cold Outreach", status: "New", created_at: "2026-05-22T14:00:00.000Z", value: "85000" },
  { id: "1716465600000", name: "Peter Parker", company: "Daily Bugle", email: "peter.parker@dailybugle.com", phone: "555-1234", source: "Website", status: "Won", created_at: "2026-05-23T11:45:00.000Z", value: "15000" },
  { id: "1716466800000", name: "Michael Scott", company: "Dunder Mifflin", email: "mscott@dundermifflin.com", phone: "555-9876", source: "Partner", status: "Lost", created_at: "2026-05-23T12:00:00.000Z", value: "4500" },
  { id: "1716468000000", name: "Ted Logan", company: "Wyld Stallyns", email: "ted@wyldstallyns.com", phone: "555-1989", source: "Referral", status: "Qualified", created_at: "2026-05-23T12:15:00.000Z", value: "32000" },
  { id: "1716469200000", name: "Sarah Connor", company: "Cyberdyne Systems", email: "sconnor@cyberdyne.co", phone: "555-2029", source: "Cold Outreach", status: "Proposal", created_at: "2026-05-23T12:30:00.000Z", value: "175000" }
];

const MOCK_DEALS = [
  { id: "d1", title: "Cloud Infrastructure Migration", lead_id: "1716462000000", value: "1250000", stage: "Qualified", close_date: "2026-06-30", created_at: "2026-05-20T09:30:00.000Z" },
  { id: "d2", title: "Arc Reactor Fusion Integration", lead_id: "1716463200000", value: "2500000", stage: "Proposal", close_date: "2026-07-15", created_at: "2026-05-21T10:15:00.000Z" },
  { id: "d3", title: "Cyberdyne Security Shield Project", lead_id: "1716469200000", value: "850000", stage: "New", close_date: "2026-06-15", created_at: "2026-05-22T14:00:00.000Z" },
  { id: "d4", title: "Bugle Ads Campaign Setup", lead_id: "1716465600000", value: "150000", stage: "Won", close_date: "2026-05-28", created_at: "2026-05-23T11:45:00.000Z" },
  { id: "d5", title: "Paper Supply Contract Renewal", lead_id: "1716466800000", value: "45000", stage: "Lost", close_date: "2026-05-25", created_at: "2026-05-23T12:00:00.000Z" }
];

const MOCK_ACTIVITIES = [
  { id: "a1", lead_id: "1716462000000", type: "Call", note: "Discussed data server architecture. Bruce requested an NDA proposal before final sign off.", date_time: "2026-05-23T10:00:00.000Z", created_at: "2026-05-23T10:00:00.000Z" },
  { id: "a2", lead_id: "1716463200000", type: "Meeting", note: "On-site review of the energy grids integrations. Tony Stark was pleased with mock results.", date_time: "2026-05-22T15:30:00.000Z", created_at: "2026-05-22T15:30:00.000Z" },
  { id: "a3", lead_id: "1716464400000", type: "Email", note: "Sent corporate presentation and security logs to Lex. Awaiting compliance approval.", date_time: "2026-05-22T09:00:00.000Z", created_at: "2026-05-22T09:00:00.000Z" }
];

const MOCK_REMINDERS_V2 = [
  { id: "r1", lead_id: "1716462000000", note: "Call Bruce Wayne to finalize cloud pricing terms", due_date: "2026-05-22", priority: "High", done: false },
  { id: "r2", lead_id: "1716463200000", note: "Send tech specifications overview to Tony Stark", due_date: "2026-05-23", priority: "High", done: false },
  { id: "r3", lead_id: "1716464400000", note: "Arrange compliance security audit call with LexCorp IT", due_date: "2026-05-25", priority: "Medium", done: false },
  { id: "r4", lead_id: "1716465600000", note: "Send contract feedback files to Daily Bugle team", due_date: "2026-05-24", priority: "Low", done: true }
];

function App() {
  const [leads, setLeads] = useState([]);
  const [deals, setDeals] = useState([]);
  const [activities, setActivities] = useState([]);
  const [reminders, setReminders] = useState([]);

  const [currentView, setCurrentView] = useState(localStorage.getItem("crm_api_url") ? "dashboard" : "settings");
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [activityTypeFilter, setActivityTypeFilter] = useState("All");

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [drawerType, setDrawerType] = useState("lead");

  const [editingLead, setEditingLead] = useState(null);
  const [viewingLead, setViewingLead] = useState(null);
  const [toasts, setToasts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const [crmApiUrl, setCrmApiUrl] = useState(localStorage.getItem("crm_api_url") || "");
  const [apiUrlInput, setApiUrlInput] = useState(localStorage.getItem("crm_api_url") || "");
  const [connectionStatus, setConnectionStatus] = useState("not_set");
  const [testConnResult, setTestConnResult] = useState(null);

  const [draggedDealId, setDraggedDealId] = useState(null);
  const [dragTargetStage, setDragTargetStage] = useState(null);
  const [doneCollapsed, setDoneCollapsed] = useState(true);

  const [leadFormData, setLeadFormData] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    source: "Website",
    status: "New",
    value: "15000"
  });

  const [dealFormData, setDealFormData] = useState({
    title: "",
    lead_id: "",
    value: "100000",
    stage: "New",
    close_date: ""
  });

  const [activityFormData, setActivityFormData] = useState({
    lead_id: "",
    type: "Call",
    note: "",
    date_time: ""
  });

  const [reminderFormData, setReminderFormData] = useState({
    lead_id: "",
    note: "",
    due_date: "",
    priority: "High"
  });

  const showToast = (type, title, message) => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { id, type, title, message }]);
    setTimeout(() => {
      setToasts(prev => prev.map(t => t.id === id ? { ...t, removing: true } : t));
      setTimeout(() => {
        setToasts(prev => prev.filter(t => t.id !== id));
      }, 300);
    }, 3000);
  };

  const parseApiResponse = (data) => {
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.values)) {
      const rows = data.values;
      if (rows.length > 1) {
        const headers = rows[0];
        return rows.slice(1).map(r => {
          const obj = {};
          headers.forEach((h, idx) => {
            obj[h] = r[idx];
          });
          return obj;
        });
      }
      return [];
    }
    if (data && data.status === "success" && Array.isArray(data.data)) {
      return data.data;
    }
    return [];
  };

  const testConnectionOnStartup = async () => {
    if (!crmApiUrl) {
      setConnectionStatus("not_set");
      return;
    }
    try {
      const res = await fetch(`${crmApiUrl}?sheet=Leads`);
      if (res.ok) {
        setConnectionStatus("connected");
      } else {
        setConnectionStatus("failed");
      }
    } catch (e) {
      setConnectionStatus("failed");
    }
  };

  const sanitizeActivities = (rawList) => {
    return (rawList || []).map(a => ({
      ...a,
      type: a.type || "Call",
      note: a.note || a.details || "Interaction logged",
      date_time: a.date_time || a.created_at || new Date().toISOString(),
      created_at: a.created_at || new Date().toISOString()
    }));
  };

  const sanitizeReminders = (rawList, currentLeads = leads) => {
    return (rawList || []).map(r => {
      let matchedLeadId = r.lead_id;
      if (!matchedLeadId && r.lead_name) {
        const found = currentLeads.find(l => l.name === r.lead_name);
        if (found) matchedLeadId = found.id;
      }
      return {
        ...r,
        lead_id: matchedLeadId || (currentLeads[0]?.id || "1716462000000"),
        note: r.note || r.text || "Follow-up note",
        priority: r.priority || "High",
        done: r.done === "true" || r.done === true || r.completed === "true" || r.completed === true || false
      };
    });
  };

  const fetchCrmData = async () => {
    setLoading(true);
    if (!crmApiUrl) {
      setConnectionStatus("not_set");
      const storedLeads = localStorage.getItem("sales_crm_leads");
      const storedDeals = localStorage.getItem("sales_crm_deals");
      const storedActivities = localStorage.getItem("sales_crm_activities");
      const storedReminders = localStorage.getItem("sales_crm_reminders");

      let currentLeads = MOCK_LEADS;
      if (storedLeads) {
        currentLeads = JSON.parse(storedLeads);
        setLeads(currentLeads);
      } else {
        setLeads(MOCK_LEADS);
        localStorage.setItem("sales_crm_leads", JSON.stringify(MOCK_LEADS));
      }

      if (storedDeals) setDeals(JSON.parse(storedDeals));
      else {
        setDeals(MOCK_DEALS);
        localStorage.setItem("sales_crm_deals", JSON.stringify(MOCK_DEALS));
      }

      if (storedActivities) {
        setActivities(sanitizeActivities(JSON.parse(storedActivities)));
      } else {
        setActivities(sanitizeActivities(MOCK_ACTIVITIES));
        localStorage.setItem("sales_crm_activities", JSON.stringify(MOCK_ACTIVITIES));
      }

      if (storedReminders) {
        setReminders(sanitizeReminders(JSON.parse(storedReminders), currentLeads));
      } else {
        setReminders(sanitizeReminders(MOCK_REMINDERS_V2, currentLeads));
        localStorage.setItem("sales_crm_reminders", JSON.stringify(MOCK_REMINDERS_V2));
      }

      showToast("info", "Offline Sandbox Mode", "Configure an Apps Script URL in Settings to synchronize");
      setLoading(false);
      return;
    }

    try {
      const leadsRes = await fetch(`${crmApiUrl}?sheet=Leads`);
      let currentLeads = [];
      if (leadsRes.ok) {
        const raw = await leadsRes.json();
        currentLeads = parseApiResponse(raw);
        setLeads(currentLeads);
        localStorage.setItem("sales_crm_leads", JSON.stringify(currentLeads));
      } else {
        currentLeads = localStorage.getItem("sales_crm_leads") ? JSON.parse(localStorage.getItem("sales_crm_leads")) : MOCK_LEADS;
      }

      const dealsRes = await fetch(`${crmApiUrl}?sheet=Deals`);
      if (dealsRes.ok) {
        const raw = await dealsRes.json();
        const loadedDeals = parseApiResponse(raw);
        setDeals(loadedDeals);
        localStorage.setItem("sales_crm_deals", JSON.stringify(loadedDeals));
      }

      const actsRes = await fetch(`${crmApiUrl}?sheet=ActivityLog`);
      if (actsRes.ok) {
        const raw = await actsRes.json();
        const loadedActivities = sanitizeActivities(parseApiResponse(raw));
        loadedActivities.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        setActivities(loadedActivities);
        localStorage.setItem("sales_crm_activities", JSON.stringify(loadedActivities));
      }

      const remRes = await fetch(`${crmApiUrl}?sheet=Reminders`);
      if (remRes.ok) {
        const raw = await remRes.json();
        const loadedReminders = sanitizeReminders(parseApiResponse(raw), currentLeads);
        setReminders(loadedReminders);
        localStorage.setItem("sales_crm_reminders", JSON.stringify(loadedReminders));
      }

      setConnectionStatus("connected");
      showToast("success", "Synchronized", "CRM records refreshed from API");
    } catch (err) {
      setConnectionStatus("failed");
      const storedLeads = localStorage.getItem("sales_crm_leads") ? JSON.parse(localStorage.getItem("sales_crm_leads")) : MOCK_LEADS;
      const storedDeals = localStorage.getItem("sales_crm_deals") ? JSON.parse(localStorage.getItem("sales_crm_deals")) : MOCK_DEALS;
      const storedActivities = localStorage.getItem("sales_crm_activities") ? JSON.parse(localStorage.getItem("sales_crm_activities")) : MOCK_ACTIVITIES;
      const storedReminders = localStorage.getItem("sales_crm_reminders") ? JSON.parse(localStorage.getItem("sales_crm_reminders")) : MOCK_REMINDERS_V2;

      setLeads(storedLeads);
      setDeals(storedDeals);
      setActivities(sanitizeActivities(storedActivities));
      setReminders(sanitizeReminders(storedReminders, storedLeads));
      showToast("warning", "Connection Fail", "Using locally cached CRM profile data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    testConnectionOnStartup();
    fetchCrmData();
  }, [crmApiUrl]);

  useEffect(() => {
    const handleGlobalMouseUp = () => {
      if (draggedDealId && dragTargetStage) {
        handleUpdateDealStage(draggedDealId, dragTargetStage);
      }
      setDraggedDealId(null);
      setDragTargetStage(null);
    };
    window.addEventListener('mouseup', handleGlobalMouseUp);
    return () => window.removeEventListener('mouseup', handleGlobalMouseUp);
  }, [draggedDealId, dragTargetStage]);

  const handleUpdateDealStage = async (dealId, newStage) => {
    const targetDeal = deals.find(d => d.id === dealId);
    if (!targetDeal) return;

    const oldStage = targetDeal.stage;
    if (oldStage === newStage) return;

    const updatedDeals = deals.map(d => d.id === dealId ? { ...d, stage: newStage } : d);
    setDeals(updatedDeals);
    localStorage.setItem("sales_crm_deals", JSON.stringify(updatedDeals));

    const newActivity = {
      id: Date.now().toString(),
      lead_id: targetDeal.lead_id,
      type: "Meeting",
      note: `Advanced deal "${targetDeal.title}" from stage ${oldStage} to ${newStage}`,
      date_time: new Date().toISOString(),
      created_at: new Date().toISOString()
    };

    const updatedActivities = [newActivity, ...activities];
    setActivities(updatedActivities);
    localStorage.setItem("sales_crm_activities", JSON.stringify(updatedActivities));

    showToast("success", "Stage Moved", `Updated stage to ${newStage}`);

    if (crmApiUrl) {
      try {
        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "Deals",
            action: "update",
            id: dealId,
            row: { stage: newStage }
          })
        });

        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "ActivityLog",
            action: "insert",
            row: newActivity
          })
        });
      } catch (err) {
        showToast("warning", "Sync Fail", "Deal moved locally, pending API retry");
      }
    }
  };

  const handleSaveApiUrl = (e) => {
    e.preventDefault();
    localStorage.setItem("crm_api_url", apiUrlInput);
    setCrmApiUrl(apiUrlInput);
    showToast("success", "Settings Saved", "API URL has been updated");
  };

  const handleTestConnection = async () => {
    if (!apiUrlInput) {
      setTestConnResult("failed");
      showToast("error", "Error", "API URL cannot be blank");
      return;
    }
    setSubmitting(true);
    try {
      const res = await fetch(`${apiUrlInput}?sheet=Leads`);
      if (res.ok) {
        setTestConnResult("connected");
        setConnectionStatus("connected");
        showToast("success", "Connected", "Successfully validated dynamic API connection");
      } else {
        setTestConnResult("failed");
        setConnectionStatus("failed");
        showToast("error", "Failed", "Server responded with an error badge");
      }
    } catch (e) {
      setTestConnResult("failed");
      setConnectionStatus("failed");
      showToast("error", "Error", "Unable to establish network connection");
    } finally {
      setSubmitting(false);
    }
  };

  const handleOpenLeadDrawer = (lead = null) => {
    setDrawerType("lead");
    if (lead) {
      setEditingLead(lead);
      setLeadFormData({
        name: lead.name,
        company: lead.company,
        email: lead.email,
        phone: lead.phone,
        source: lead.source,
        status: lead.status,
        value: lead.value
      });
    } else {
      setEditingLead(null);
      setLeadFormData({
        name: "",
        company: "",
        email: "",
        phone: "",
        source: "Website",
        status: "New",
        value: "15000"
      });
    }
    setDrawerOpen(true);
  };

  const handleOpenDealDrawer = (defaultStage = "New") => {
    setDrawerType("deal");
    setDealFormData({
      title: "",
      lead_id: leads[0]?.id || "",
      value: "100000",
      stage: defaultStage,
      close_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    });
    setDrawerOpen(true);
  };

  const handleOpenActivityDrawer = () => {
    setDrawerType("activity");
    setActivityFormData({
      lead_id: leads[0]?.id || "",
      type: "Call",
      note: "",
      date_time: new Date().toISOString().slice(0, 16)
    });
    setDrawerOpen(true);
  };

  const handleOpenReminderDrawer = () => {
    setDrawerType("reminder");
    setReminderFormData({
      lead_id: leads[0]?.id || "",
      note: "",
      due_date: new Date().toISOString().split('T')[0],
      priority: "High"
    });
    setDrawerOpen(true);
  };

  const handleLeadSubmit = async (e) => {
    e.preventDefault();
    if (!leadFormData.name || !leadFormData.company || !leadFormData.email) {
      showToast("error", "Validation Error", "Please fill in all required fields (*)");
      return;
    }

    setSubmitting(true);

    if (editingLead) {
      const updatedLead = {
        ...editingLead,
        ...leadFormData
      };

      const updatedLeads = leads.map(l => l.id === editingLead.id ? updatedLead : l);
      setLeads(updatedLeads);
      localStorage.setItem("sales_crm_leads", JSON.stringify(updatedLeads));

      const newAct = {
        id: Date.now().toString(),
        lead_id: editingLead.id,
        type: "Email",
        note: `Updated contact record: ${leadFormData.name} at ${leadFormData.company}`,
        date_time: new Date().toISOString(),
        created_at: new Date().toISOString()
      };

      const updatedActivities = [newAct, ...activities];
      setActivities(updatedActivities);
      localStorage.setItem("sales_crm_activities", JSON.stringify(updatedActivities));

      showToast("success", "Saved", "Lead updated successfully");

      if (crmApiUrl) {
        try {
          await fetch(crmApiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              sheet: "Leads",
              action: "update",
              id: editingLead.id,
              row: leadFormData
            })
          });

          await fetch(crmApiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              sheet: "ActivityLog",
              action: "insert",
              row: newAct
            })
          });
        } catch (e) {
          showToast("warning", "Sync Fail", "Changes saved locally");
        }
      }
    } else {
      const newLead = {
        id: Date.now().toString(),
        ...leadFormData,
        created_at: new Date().toISOString()
      };

      const updatedLeads = [newLead, ...leads];
      setLeads(updatedLeads);
      localStorage.setItem("sales_crm_leads", JSON.stringify(updatedLeads));

      const newAct = {
        id: Date.now().toString(),
        lead_id: newLead.id,
        type: "Call",
        note: `Registered new sales lead: ${newLead.name} with ${newLead.company}`,
        date_time: new Date().toISOString(),
        created_at: new Date().toISOString()
      };

      const updatedActivities = [newAct, ...activities];
      setActivities(updatedActivities);
      localStorage.setItem("sales_crm_activities", JSON.stringify(updatedActivities));

      showToast("success", "Created", "New lead registered");

      if (crmApiUrl) {
        try {
          await fetch(crmApiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              sheet: "Leads",
              action: "insert",
              row: newLead
            })
          });

          await fetch(crmApiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              sheet: "ActivityLog",
              action: "insert",
              row: newAct
            })
          });
        } catch (e) {
          showToast("warning", "Sync Fail", "Lead added locally");
        }
      }
    }

    setDrawerOpen(false);
    setSubmitting(false);
  };

  const handleDealSubmit = async (e) => {
    e.preventDefault();
    if (!dealFormData.title || !dealFormData.lead_id || !dealFormData.value || !dealFormData.close_date) {
      showToast("error", "Validation Error", "All deal fields are required");
      return;
    }

    setSubmitting(true);

    const newDeal = {
      id: Date.now().toString(),
      ...dealFormData,
      created_at: new Date().toISOString()
    };

    const updatedDeals = [newDeal, ...deals];
    setDeals(updatedDeals);
    localStorage.setItem("sales_crm_deals", JSON.stringify(updatedDeals));

    const newAct = {
      id: Date.now().toString(),
      lead_id: dealFormData.lead_id,
      type: "Meeting",
      note: `Opened deal opportunity: "${dealFormData.title}" valued at ₹${Number(dealFormData.value).toLocaleString('en-IN')}`,
      date_time: new Date().toISOString(),
      created_at: new Date().toISOString()
    };

    const updatedActivities = [newAct, ...activities];
    setActivities(updatedActivities);
    localStorage.setItem("sales_crm_activities", JSON.stringify(updatedActivities));

    showToast("success", "Deal Added", "New deal saved to pipeline");

    if (crmApiUrl) {
      try {
        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "Deals",
            action: "insert",
            row: newDeal
          })
        });

        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "ActivityLog",
            action: "insert",
            row: newAct
          })
        });
      } catch (err) {
        showToast("warning", "Sync Fail", "Deal logged locally");
      }
    }

    setDrawerOpen(false);
    setSubmitting(false);
  };

  const handleActivitySubmit = async (e) => {
    e.preventDefault();
    if (!activityFormData.lead_id || !activityFormData.note || !activityFormData.date_time) {
      showToast("error", "Validation Error", "All activity log fields are required");
      return;
    }

    setSubmitting(true);

    const newAct = {
      id: Date.now().toString(),
      lead_id: activityFormData.lead_id,
      type: activityFormData.type,
      note: activityFormData.note,
      date_time: new Date(activityFormData.date_time).toISOString(),
      created_at: new Date().toISOString()
    };

    const updatedActivities = [newAct, ...activities];
    setActivities(updatedActivities);
    localStorage.setItem("sales_crm_activities", JSON.stringify(updatedActivities));

    showToast("success", "Activity Logged", "Timeline updated");

    if (crmApiUrl) {
      try {
        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "ActivityLog",
            action: "insert",
            row: newAct
          })
        });
      } catch (err) {
        showToast("warning", "Sync Fail", "Activity saved locally");
      }
    }

    setDrawerOpen(false);
    setSubmitting(false);
  };

  const handleReminderSubmit = async (e) => {
    e.preventDefault();
    if (!reminderFormData.lead_id || !reminderFormData.note || !reminderFormData.due_date) {
      showToast("error", "Validation Error", "All fields are required");
      return;
    }

    setSubmitting(true);

    const newReminder = {
      id: Date.now().toString(),
      lead_id: reminderFormData.lead_id,
      note: reminderFormData.note,
      due_date: reminderFormData.due_date,
      priority: reminderFormData.priority,
      done: false
    };

    const updated = [newReminder, ...reminders];
    setReminders(updated);
    localStorage.setItem("sales_crm_reminders", JSON.stringify(updated));

    showToast("success", "Reminder Saved", "New task scheduled");

    if (crmApiUrl) {
      try {
        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "Reminders",
            action: "insert",
            row: newReminder
          })
        });
      } catch (err) {
        showToast("warning", "Sync Fail", "Reminder saved locally");
      }
    }

    setDrawerOpen(false);
    setSubmitting(false);
  };

  const handleMarkReminderDone = async (remId) => {
    const targetRem = reminders.find(r => r.id === remId);
    if (!targetRem) return;

    const updated = reminders.map(r => r.id === remId ? { ...r, done: true } : r);
    setReminders(updated);
    localStorage.setItem("sales_crm_reminders", JSON.stringify(updated));

    showToast("success", "Reminder Done", "Task completed");

    if (crmApiUrl) {
      try {
        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "Reminders",
            action: "update",
            id: remId,
            row: { done: true }
          })
        });
      } catch (err) {
        showToast("warning", "Sync Fail", "Reminder updated locally");
      }
    }
  };

  const handleDeleteLead = async (leadId) => {
    const targetLead = leads.find(l => l.id === leadId);
    if (!targetLead) return;

    if (!window.confirm(`Are you sure you want to delete ${targetLead.name}?`)) {
      return;
    }

    const updatedLeads = leads.filter(l => l.id !== leadId);
    setLeads(updatedLeads);
    localStorage.setItem("sales_crm_leads", JSON.stringify(updatedLeads));

    const newAct = {
      id: Date.now().toString(),
      lead_id: leadId,
      type: "Call",
      note: `Deleted lead contact: ${targetLead.name}`,
      date_time: new Date().toISOString(),
      created_at: new Date().toISOString()
    };

    const updatedActivities = [newAct, ...activities];
    setActivities(updatedActivities);
    localStorage.setItem("sales_crm_activities", JSON.stringify(updatedActivities));

    showToast("success", "Lead Removed", "Deleted lead record");

    if (crmApiUrl) {
      try {
        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "Leads",
            action: "delete",
            id: leadId
          })
        });

        await fetch(crmApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sheet: "ActivityLog",
            action: "insert",
            row: newAct
          })
        });
      } catch (err) {
        showToast("warning", "Sync Fail", "Lead removed locally");
      }
    }
  };

  const formatRupee = (val) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(val);
  };

  const getKPIs = () => {
    const totalLeads = leads.length;
    const activeDeals = deals.filter(d => d.stage === "New" || d.stage === "Qualified" || d.stage === "Proposal").length;

    const todayStr = new Date().toISOString().split('T')[0];
    const followupsDue = reminders.filter(r => r.due_date === todayStr && !r.done).length;

    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    const wonThisMonth = deals.filter(d => {
      if (d.stage !== "Won") return false;
      const date = new Date(d.created_at);
      return date.getMonth() === currentMonth && date.getFullYear() === currentYear;
    }).length;

    return { totalLeads, activeDeals, followupsDue, wonThisMonth };
  };

  const kpis = getKPIs();

  const getFilteredLeads = () => {
    return leads.filter(lead => {
      const query = searchQuery.toLowerCase();
      const matchesSearch =
        lead.name.toLowerCase().includes(query) ||
        lead.company.toLowerCase().includes(query) ||
        lead.email.toLowerCase().includes(query);
      const matchesStatus = statusFilter === "all" || lead.status.toLowerCase() === statusFilter.toLowerCase();
      return matchesSearch && matchesStatus;
    });
  };

  const getFilteredActivities = () => {
    if (activityTypeFilter === "All") return activities;
    return activities.filter(act => act.type === activityTypeFilter);
  };

  const getGroupedReminders = () => {
    const todayStr = new Date().toISOString().split('T')[0];
    const activeReminders = reminders.filter(r => !r.done);
    const completedReminders = reminders.filter(r => r.done);

    const overdue = activeReminders.filter(r => r.due_date < todayStr);
    const today = activeReminders.filter(r => r.due_date === todayStr);
    const upcoming = activeReminders.filter(r => r.due_date > todayStr);

    return { overdue, today, upcoming, doneList: completedReminders };
  };

  const filteredLeads = getFilteredLeads();
  const filteredActivities = getFilteredActivities();
  const groupedReminders = getGroupedReminders();

  return (
    <div className="app-container">
      <div className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`} onClick={() => setSidebarOpen(false)}></div>

      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-brand">
          <div className="sidebar-logo">
            <TrendingUp size={28} />
          </div>
          <span className="sidebar-title">SalesCRM</span>
        </div>

        <nav className="sidebar-nav">
          <div
            className={`sidebar-item ${currentView === "dashboard" ? "active" : ""}`}
            onClick={() => { setCurrentView("dashboard"); setViewingLead(null); setSidebarOpen(false); }}
            id="nav-dashboard"
          >
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
          </div>
          <div
            className={`sidebar-item ${currentView === "leads" ? "active" : ""}`}
            onClick={() => { setCurrentView("leads"); setViewingLead(null); setSidebarOpen(false); }}
            id="nav-leads"
          >
            <Users size={20} />
            <span>Leads</span>
          </div>
          <div
            className={`sidebar-item ${currentView === "pipeline" ? "active" : ""}`}
            onClick={() => { setCurrentView("pipeline"); setViewingLead(null); setSidebarOpen(false); }}
            id="nav-pipeline"
          >
            <KanbanSquare size={20} />
            <span>Pipeline</span>
          </div>
          <div
            className={`sidebar-item ${currentView === "activity" ? "active" : ""}`}
            onClick={() => { setCurrentView("activity"); setViewingLead(null); setSidebarOpen(false); }}
            id="nav-activity"
          >
            <History size={20} />
            <span>Activity</span>
          </div>
          <div
            className={`sidebar-item ${currentView === "reminders" ? "active" : ""}`}
            onClick={() => { setCurrentView("reminders"); setViewingLead(null); setSidebarOpen(false); }}
            id="nav-reminders"
          >
            <CalendarClock size={20} />
            <span>Reminders</span>
          </div>
          <div
            className={`sidebar-item ${currentView === "settings" ? "active" : ""}`}
            onClick={() => { setCurrentView("settings"); setViewingLead(null); setSidebarOpen(false); }}
            id="nav-settings"
          >
            <Settings size={20} />
            <span>Settings</span>
          </div>
        </nav>

        <div className="sidebar-status-box">
          <span className={`status-dot ${connectionStatus === "connected" ? "status-dot-green" : "status-dot-red"}`}></span>
          <span className="sidebar-status-lbl">
            {connectionStatus === "connected" && "Connected"}
            {connectionStatus === "failed" && "Sync Failed"}
            {connectionStatus === "not_set" && "Offline Sandbox"}
          </span>
        </div>

        <div className="sidebar-user">
          <div className="avatar">JD</div>
          <div className="user-info">
            <span className="user-name">John Doe</span>
            <span className="user-role">Enterprise Account Executive</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="header">
          <div className="header-left">
            <button className="sidebar-toggle" onClick={() => setSidebarOpen(true)} id="btn-sidebar-toggle">
              <Menu size={24} />
            </button>
            <h1 className="header-title" id="crm-main-title">
              {viewingLead ? "Lead Profile Details" :
                currentView === "reminders" ? "Reminders View" :
                  currentView === "settings" ? "Settings Panel" :
                    currentView.charAt(0).toUpperCase() + currentView.slice(1)}
            </h1>
          </div>
          <div className="header-right">
            <span className="header-date">
              {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' })}
            </span>
            {currentView === "leads" && !viewingLead && (
              <button className="btn btn-primary" onClick={() => handleOpenLeadDrawer()} id="btn-add-lead">
                <Plus size={16} />
                <span>Add Lead</span>
              </button>
            )}
            {currentView === "activity" && (
              <button className="btn btn-primary" onClick={handleOpenActivityDrawer} id="btn-log-activity">
                <Plus size={16} />
                <span>Log Activity</span>
              </button>
            )}
            {currentView === "reminders" && (
              <button className="btn btn-primary" onClick={handleOpenReminderDrawer} id="btn-add-reminder">
                <Plus size={16} />
                <span>Add Reminder</span>
              </button>
            )}
          </div>
        </header>

        <div className="view-content">
          {viewingLead ? (
            <div className="detail-view">
              <div className="detail-header">
                <div className="detail-title-block">
                  <div className="detail-profile-circle">
                    {viewingLead.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <h2 className="detail-name">{viewingLead.name}</h2>
                    <p className="detail-company">{viewingLead.company}</p>
                  </div>
                </div>
                <div className="action-buttons">
                  <button className="btn btn-secondary" onClick={() => setViewingLead(null)}>Back to list</button>
                  <button className="btn btn-primary" onClick={() => { handleOpenLeadDrawer(viewingLead); setViewingLead(null); }}>Edit Lead</button>
                </div>
              </div>
              <div className="detail-grid">
                <div className="detail-group">
                  <span className="detail-label">Email Address</span>
                  <span className="detail-value">{viewingLead.email}</span>
                </div>
                <div className="detail-group">
                  <span className="detail-label">Phone Number</span>
                  <span className="detail-value">{viewingLead.phone || "Not specified"}</span>
                </div>
                <div className="detail-group">
                  <span className="detail-label">Pipeline Status</span>
                  <div>
                    <span className={`badge badge-${viewingLead.status.toLowerCase()}`}>{viewingLead.status}</span>
                  </div>
                </div>
                <div className="detail-group">
                  <span className="detail-label">Lead Source</span>
                  <span className="detail-value">{viewingLead.source}</span>
                </div>
                <div className="detail-group">
                  <span className="detail-label">Expected Deal Value</span>
                  <span className="detail-value">{formatRupee(viewingLead.value)}</span>
                </div>
                <div className="detail-group">
                  <span className="detail-label">Created Date</span>
                  <span className="detail-value">{new Date(viewingLead.created_at).toLocaleString()}</span>
                </div>
              </div>
            </div>
          ) : (
            <>
              {currentView === "dashboard" && (
                <div>
                  <div className="grid-kpi">
                    <div className="kpi-card">
                      <div className="kpi-icon-wrapper" style={{ backgroundColor: "#EEF2FF", color: "#6366F1" }}>
                        <Users size={24} />
                      </div>
                      <div className="kpi-details">
                        <span className="kpi-title">Total Leads</span>
                        <span className="kpi-value" id="kpi-total-leads">{kpis.totalLeads}</span>
                      </div>
                    </div>

                    <div className="kpi-card">
                      <div className="kpi-icon-wrapper" style={{ backgroundColor: "#EFF6FF", color: "#3B82F6" }}>
                        <Briefcase size={24} />
                      </div>
                      <div className="kpi-details">
                        <span className="kpi-title">Active Deals</span>
                        <span className="kpi-value" id="kpi-active-deals">{kpis.activeDeals}</span>
                      </div>
                    </div>

                    <div className="kpi-card">
                      <div className="kpi-icon-wrapper" style={{ backgroundColor: "#FEF3C7", color: "#D97706" }}>
                        <CalendarClock size={24} />
                      </div>
                      <div className="kpi-details">
                        <span className="kpi-title">Follow-ups Today</span>
                        <span className="kpi-value" id="kpi-followups">{kpis.followupsDue}</span>
                      </div>
                    </div>

                    <div className="kpi-card">
                      <div className="kpi-icon-wrapper" style={{ backgroundColor: "#ECFDF5", color: "#10B981" }}>
                        <TrendingUp size={24} />
                      </div>
                      <div className="kpi-details">
                        <span className="kpi-title">Won This Month</span>
                        <span className="kpi-value" id="kpi-won">{kpis.wonThisMonth}</span>
                      </div>
                    </div>
                  </div>

                  <div className="dashboard-split">
                    <div className="card">
                      <div className="card-header">
                        <h2 className="card-title">Top Active Leads</h2>
                        <span className="view-all-link" onClick={() => setCurrentView("leads")}>View Leads</span>
                      </div>

                      <div className="table-responsive">
                        {loading ? (
                          Array.from({ length: 3 }).map((_, i) => (
                            <div className="skeleton-row" key={i}>
                              <div className="skeleton-bar" style={{ width: "25%", marginRight: "10%" }}></div>
                              <div className="skeleton-bar" style={{ width: "35%", marginRight: "10%" }}></div>
                              <div className="skeleton-bar" style={{ width: "15%", marginRight: "10%" }}></div>
                              <div className="skeleton-bar" style={{ width: "10%" }}></div>
                            </div>
                          ))
                        ) : leads.length === 0 ? (
                          <div className="empty-state">
                            <Users size={36} className="empty-state-icon" />
                            <h3 className="empty-state-title">No leads in pipeline</h3>
                            <p className="empty-state-desc">Start adding new leads to visualize the sales tracker.</p>
                          </div>
                        ) : (
                          <table className="crm-table">
                            <thead>
                              <tr>
                                <th>Name</th>
                                <th>Company</th>
                                <th>Status</th>
                                <th>Value</th>
                              </tr>
                            </thead>
                            <tbody>
                              {leads.slice(0, 5).map(lead => (
                                <tr key={lead.id}>
                                  <td className="lead-name-cell">{lead.name}</td>
                                  <td className="lead-company-cell">{lead.company}</td>
                                  <td>
                                    <span className={`badge badge-${lead.status.toLowerCase()}`}>{lead.status}</span>
                                  </td>
                                  <td style={{ fontWeight: 600 }}>{formatRupee(lead.value)}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        )}
                      </div>
                    </div>

                    <div className="card">
                      <div className="card-header">
                        <h2 className="card-title">Recent Activity Feed</h2>
                        <span className="view-all-link" onClick={() => setCurrentView("activity")}>Full history</span>
                      </div>

                      <div className="activity-list">
                        {loading ? (
                          Array.from({ length: 3 }).map((_, i) => (
                            <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }} key={i}>
                              <div className="skeleton-bar" style={{ width: "24px", height: "24px", borderRadius: "50%" }}></div>
                              <div style={{ flex: 1 }}>
                                <div className="skeleton-bar" style={{ width: "80%", height: "10px", marginBottom: "6px" }}></div>
                                <div className="skeleton-bar" style={{ width: "40%", height: "8px" }}></div>
                              </div>
                            </div>
                          ))
                        ) : activities.length === 0 ? (
                          <div className="empty-state">
                            <History size={36} className="empty-state-icon" />
                            <h3 className="empty-state-title">No activities logged</h3>
                            <p className="empty-state-desc">Actions will appear here as you log sales deals.</p>
                          </div>
                        ) : (
                          activities.slice(0, 5).map(act => {
                            const relatedLead = leads.find(l => l.id === act.lead_id);
                            const actType = act.type || "Call";
                            return (
                              <div className="activity-item" key={act.id}>
                                <div className="activity-bullet" style={{
                                  backgroundColor: actType === "Call" ? "#DBEAFE" :
                                    actType === "Email" ? "#E0E7FF" : "#D1FAE5",
                                  color: actType === "Call" ? "#1E40AF" :
                                    actType === "Email" ? "#3730A3" : "#065F46"
                                }}>
                                  <span style={{ fontSize: "12px" }}>
                                    {actType === "Call" && "📞"}
                                    {actType === "Email" && "📧"}
                                    {actType === "Meeting" && "🤝"}
                                  </span>
                                </div>
                                <div className="activity-content">
                                  <span className="activity-desc">
                                    <span>{relatedLead ? relatedLead.name : "Unknown Contact"}</span> - {act.note}
                                  </span>
                                  <span className="activity-time">{new Date(act.date_time || act.created_at).toLocaleString('en-US', { dateStyle: 'short', timeStyle: 'short' })}</span>
                                </div>
                              </div>
                            );
                          })
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {currentView === "leads" && (
                <div className="card">
                  <div className="filters-bar">
                    <div className="filters-left">
                      <div className="search-input-wrapper">
                        <Search size={18} className="search-icon" />
                        <input
                          type="text"
                          className="form-input"
                          placeholder="Search leads, companies or emails..."
                          value={searchQuery}
                          onChange={(e) => setSearchQuery(e.target.value)}
                          id="search-leads"
                        />
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                        <Filter size={16} style={{ color: "#64748B" }} />
                        <select
                          className="form-select"
                          value={statusFilter}
                          onChange={(e) => setStatusFilter(e.target.value)}
                          id="filter-status"
                        >
                          <option value="all">All Statuses</option>
                          <option value="New">New</option>
                          <option value="Qualified">Qualified</option>
                          <option value="Proposal">Proposal</option>
                          <option value="Won">Won</option>
                          <option value="Lost">Lost</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <div className="table-responsive">
                    {loading ? (
                      Array.from({ length: 4 }).map((_, i) => (
                        <div className="skeleton-row" key={i}>
                          <div className="skeleton-bar" style={{ width: "20%", marginRight: "5%" }}></div>
                          <div className="skeleton-bar" style={{ width: "20%", marginRight: "5%" }}></div>
                          <div className="skeleton-bar" style={{ width: "25%", marginRight: "5%" }}></div>
                          <div className="skeleton-bar" style={{ width: "10%", marginRight: "5%" }}></div>
                          <div className="skeleton-bar" style={{ width: "10%", marginRight: "5%" }}></div>
                          <div className="skeleton-bar" style={{ width: "10%" }}></div>
                        </div>
                      ))
                    ) : filteredLeads.length === 0 ? (
                      <div className="empty-state">
                        <Users size={36} className="empty-state-icon" />
                        <h3 className="empty-state-title">No leads matching filters</h3>
                        <p className="empty-state-desc">Try modifying your query or select a different pipeline stage.</p>
                      </div>
                    ) : (
                      <table className="crm-table">
                        <thead>
                          <tr>
                            <th>Name</th>
                            <th>Company</th>
                            <th>Email</th>
                            <th>Status</th>
                            <th>Source</th>
                            <th>Value</th>
                            <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {filteredLeads.map(lead => (
                            <tr key={lead.id}>
                              <td className="lead-name-cell">{lead.name}</td>
                              <td>{lead.company}</td>
                              <td>{lead.email}</td>
                              <td>
                                <span className={`badge badge-${lead.status.toLowerCase()}`}>{lead.status}</span>
                              </td>
                              <td style={{ textTransform: "capitalize" }}>{lead.source}</td>
                              <td style={{ fontWeight: 600 }}>{formatRupee(lead.value)}</td>
                              <td>
                                <div className="action-buttons">
                                  <button className="btn-icon" onClick={() => setViewingLead(lead)} title="View Profile">
                                    <Eye size={16} />
                                  </button>
                                  <button className="btn-icon" onClick={() => handleOpenLeadDrawer(lead)} title="Edit Lead">
                                    <Pencil size={16} />
                                  </button>
                                  <button className="btn-icon btn-icon-delete" onClick={() => handleDeleteLead(lead.id)} title="Delete Lead">
                                    <Trash2 size={16} />
                                  </button>
                                </div>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                </div>
              )}

              {currentView === "pipeline" && (
                <div className="pipeline-board">
                  {["New", "Qualified", "Proposal", "Won", "Lost"].map(status => {
                    const statusDeals = deals.filter(d => d.stage === status);
                    const totalValue = statusDeals.reduce((acc, curr) => acc + Number(curr.value || 0), 0);
                    const isDragOver = dragTargetStage === status;

                    return (
                      <div
                        className={`pipeline-column ${isDragOver ? "drag-over" : ""}`}
                        key={status}
                        onMouseEnter={() => {
                          if (draggedDealId) {
                            setDragTargetStage(status);
                          }
                        }}
                      >
                        <div className="pipeline-col-header">
                          <div className="pipeline-col-title-wrapper">
                            <span className="pipeline-col-indicator" style={{
                              backgroundColor: status === "New" ? "#3B82F6" :
                                status === "Qualified" ? "#6366F1" :
                                  status === "Proposal" ? "#F59E0B" :
                                    status === "Won" ? "#10B981" : "#EF4444"
                            }}></span>
                            <span className="pipeline-col-title">{status}</span>
                            <span className="pipeline-col-count">{statusDeals.length}</span>
                          </div>
                          <button
                            className="btn-icon"
                            onClick={() => handleOpenDealDrawer(status)}
                            title="Add Deal"
                            style={{ width: "24px", height: "24px" }}
                          >
                            <Plus size={14} />
                          </button>
                        </div>
                        <div className="pipeline-col-value">{formatRupee(totalValue)}</div>

                        {statusDeals.length === 0 ? (
                          <div style={{ flex: 1, border: "2px dashed #E2E8F0", borderRadius: "0.75rem", display: "flex", alignItems: "center", justifyContent: "center", minHeight: "150px", color: "#94A3B8", fontSize: "0.75rem" }}>
                            Empty Stage
                          </div>
                        ) : (
                          statusDeals.map(deal => {
                            const relatedLead = leads.find(l => l.id === deal.lead_id);
                            const isDragging = draggedDealId === deal.id;
                            return (
                              <div
                                className={`pipeline-card ${isDragging ? "dragging" : ""}`}
                                key={deal.id}
                                style={{
                                  borderLeftColor: status === "New" ? "#3B82F6" :
                                    status === "Qualified" ? "#6366F1" :
                                      status === "Proposal" ? "#F59E0B" :
                                        status === "Won" ? "#10B981" : "#EF4444"
                                }}
                                onMouseDown={(e) => {
                                  if (e.button === 0) {
                                    e.stopPropagation();
                                    setDraggedDealId(deal.id);
                                    setDragTargetStage(status);
                                  }
                                }}
                              >
                                <span className="pipeline-card-company">{relatedLead ? relatedLead.company : "Unknown Company"}</span>
                                <div className="pipeline-card-name">{deal.title}</div>
                                <div className="pipeline-card-footer">
                                  <span className="pipeline-card-value">{formatRupee(deal.value)}</span>
                                  <span className="pipeline-card-date">{deal.close_date}</span>
                                </div>
                              </div>
                            );
                          })
                        )}
                      </div>
                    );
                  })}
                </div>
              )}

              {currentView === "activity" && (
                <div>
                  <div className="pill-container">
                    {["All", "Call", "Email", "Meeting"].map(type => (
                      <button
                        key={type}
                        className={`pill-btn ${activityTypeFilter === type ? "active" : ""}`}
                        onClick={() => setActivityTypeFilter(type)}
                      >
                        {type === "All" && "⭐ All"}
                        {type === "Call" && "📞 Calls"}
                        {type === "Email" && "📧 Emails"}
                        {type === "Meeting" && "🤝 Meetings"}
                      </button>
                    ))}
                  </div>

                  <div className="timeline-container">
                    <div className="timeline-line"></div>
                    {loading ? (
                      Array.from({ length: 3 }).map((_, i) => (
                        <div className="timeline-item" key={i}>
                          <div className="timeline-dot" style={{ backgroundColor: "#E2E8F0" }}></div>
                          <div className="timeline-card">
                            <div className="skeleton-bar" style={{ width: "40%", height: "14px", marginBottom: "8px" }}></div>
                            <div className="skeleton-bar" style={{ width: "70%", height: "10px" }}></div>
                          </div>
                        </div>
                      ))
                    ) : filteredActivities.length === 0 ? (
                      <div className="empty-state" style={{ paddingLeft: "0" }}>
                        <History size={48} className="empty-state-icon" />
                        <h3 className="empty-state-title">No matching activity records</h3>
                        <p className="empty-state-desc">Log a phone call, email sync, or client sync using the "+ Log Activity" header button.</p>
                      </div>
                    ) : (
                      filteredActivities.map(act => {
                        const relatedLead = leads.find(l => l.id === act.lead_id);
                        const actType = act.type || "Call";
                        return (
                          <div className="timeline-item" key={act.id}>
                            <div className={`timeline-dot timeline-dot-${actType.toLowerCase()}`}></div>
                            <div className="timeline-card">
                              <div className="timeline-header">
                                <div className="timeline-title">
                                  <span>
                                    {actType === "Call" && "📞"}
                                    {actType === "Email" && "📧"}
                                    {actType === "Meeting" && "🤝"}
                                  </span>
                                  <span>{actType} with <strong>{relatedLead ? relatedLead.name : "Unknown Client"}</strong></span>
                                  {relatedLead && <span style={{ fontSize: "11px", color: "var(--text-muted)", fontWeight: "normal" }}>({relatedLead.company})</span>}
                                </div>
                                <span className="timeline-date">
                                  {new Date(act.date_time || act.created_at).toLocaleString('en-IN', {
                                    dateStyle: 'medium',
                                    timeStyle: 'short'
                                  })}
                                </span>
                              </div>
                              <div className="timeline-note">{act.note}</div>
                            </div>
                          </div>
                        );
                      })
                    )}
                  </div>
                </div>
              )}

              {currentView === "reminders" && (
                <div className="reminders-view-container">
                  {loading ? (
                    Array.from({ length: 2 }).map((_, i) => (
                      <div className="reminder-group-section" key={i}>
                        <div className="skeleton-bar" style={{ width: "20%", height: "16px", marginBottom: "8px" }}></div>
                        <div className="reminder-grid">
                          <div className="reminder-card-v2">
                            <div className="skeleton-bar" style={{ width: "40%", height: "12px", marginBottom: "6px" }}></div>
                            <div className="skeleton-bar" style={{ width: "90%", height: "10px" }}></div>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <>
                      <div className="reminder-group-section">
                        <div className="reminder-group-header">
                          <span className="reminder-group-title overdue">Overdue</span>
                          <span className="reminder-group-badge overdue">{groupedReminders.overdue.length}</span>
                        </div>
                        {groupedReminders.overdue.length === 0 ? (
                          <div style={{ color: "var(--text-muted)", fontSize: "0.8125rem", padding: "0.5rem 0" }}>No overdue reminders</div>
                        ) : (
                          <div className="reminder-grid">
                            {groupedReminders.overdue.map(rem => {
                              const relatedLead = leads.find(l => l.id === rem.lead_id);
                              return (
                                <div className="reminder-card-v2" key={rem.id}>
                                  <div className="reminder-card-v2-header">
                                    <span className="reminder-card-v2-contact">{relatedLead ? `${relatedLead.name} (${relatedLead.company})` : "General"}</span>
                                    <span className={`reminder-priority-badge reminder-priority-${rem.priority.toLowerCase()}`}>
                                      {rem.priority}
                                    </span>
                                  </div>
                                  <div className="reminder-note-v2">{rem.note}</div>
                                  <div className="reminder-card-v2-footer">
                                    <div className="reminder-due-v2" style={{ color: "#EF4444", fontWeight: 600 }}>
                                      <Clock size={12} />
                                      <span>Due: {rem.due_date}</span>
                                    </div>
                                    <button className="btn btn-secondary" style={{ padding: "0.25rem 0.75rem", fontSize: "0.75rem" }} onClick={() => handleMarkReminderDone(rem.id)}>
                                      Mark Done
                                    </button>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>

                      <div className="reminder-group-section">
                        <div className="reminder-group-header">
                          <span className="reminder-group-title today">Today</span>
                          <span className="reminder-group-badge today">{groupedReminders.today.length}</span>
                        </div>
                        {groupedReminders.today.length === 0 ? (
                          <div style={{ color: "var(--text-muted)", fontSize: "0.8125rem", padding: "0.5rem 0" }}>No reminders due today</div>
                        ) : (
                          <div className="reminder-grid">
                            {groupedReminders.today.map(rem => {
                              const relatedLead = leads.find(l => l.id === rem.lead_id);
                              return (
                                <div className="reminder-card-v2" key={rem.id}>
                                  <div className="reminder-card-v2-header">
                                    <span className="reminder-card-v2-contact">{relatedLead ? `${relatedLead.name} (${relatedLead.company})` : "General"}</span>
                                    <span className={`reminder-priority-badge reminder-priority-${rem.priority.toLowerCase()}`}>
                                      {rem.priority}
                                    </span>
                                  </div>
                                  <div className="reminder-note-v2">{rem.note}</div>
                                  <div className="reminder-card-v2-footer">
                                    <div className="reminder-due-v2" style={{ color: "#D97706", fontWeight: 600 }}>
                                      <Clock size={12} />
                                      <span>Due: Today ({rem.due_date})</span>
                                    </div>
                                    <button className="btn btn-secondary" style={{ padding: "0.25rem 0.75rem", fontSize: "0.75rem" }} onClick={() => handleMarkReminderDone(rem.id)}>
                                      Mark Done
                                    </button>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>

                      <div className="reminder-group-section">
                        <div className="reminder-group-header">
                          <span className="reminder-group-title upcoming">Upcoming</span>
                          <span className="reminder-group-badge upcoming">{groupedReminders.upcoming.length}</span>
                        </div>
                        {groupedReminders.upcoming.length === 0 ? (
                          <div style={{ color: "var(--text-muted)", fontSize: "0.8125rem", padding: "0.5rem 0" }}>No upcoming reminders scheduled</div>
                        ) : (
                          <div className="reminder-grid">
                            {groupedReminders.upcoming.map(rem => {
                              const relatedLead = leads.find(l => l.id === rem.lead_id);
                              return (
                                <div className="reminder-card-v2" key={rem.id}>
                                  <div className="reminder-card-v2-header">
                                    <span className="reminder-card-v2-contact">{relatedLead ? `${relatedLead.name} (${relatedLead.company})` : "General"}</span>
                                    <span className={`reminder-priority-badge reminder-priority-${rem.priority.toLowerCase()}`}>
                                      {rem.priority}
                                    </span>
                                  </div>
                                  <div className="reminder-note-v2">{rem.note}</div>
                                  <div className="reminder-card-v2-footer">
                                    <div className="reminder-due-v2">
                                      <Clock size={12} />
                                      <span>Due: {rem.due_date}</span>
                                    </div>
                                    <button className="btn btn-secondary" style={{ padding: "0.25rem 0.75rem", fontSize: "0.75rem" }} onClick={() => handleMarkReminderDone(rem.id)}>
                                      Mark Done
                                    </button>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>

                      <div>
                        <div className="done-collapsible-header" onClick={() => setDoneCollapsed(!doneCollapsed)}>
                          <div className="done-collapsible-title">
                            <span>Completed Tasks ({groupedReminders.doneList.length})</span>
                          </div>
                          <div>
                            {doneCollapsed ? <ChevronDown size={20} style={{ color: "#64748B" }} /> : <ChevronUp size={20} style={{ color: "#64748B" }} />}
                          </div>
                        </div>
                        {!doneCollapsed && (
                          <div className="reminder-grid" style={{ marginTop: "1rem" }}>
                            {groupedReminders.doneList.length === 0 ? (
                              <div style={{ color: "var(--text-muted)", fontSize: "0.8125rem", padding: "0.5rem 0" }}>No completed reminders</div>
                            ) : (
                              groupedReminders.doneList.map(rem => {
                                const relatedLead = leads.find(l => l.id === rem.lead_id);
                                return (
                                  <div className="reminder-card-v2 done" key={rem.id}>
                                    <div className="reminder-card-v2-header">
                                      <span className="reminder-card-v2-contact">{relatedLead ? `${relatedLead.name} (${relatedLead.company})` : "General"}</span>
                                      <span className="reminder-priority-badge" style={{ backgroundColor: "#F1F5F9", color: "#64748B", border: "1px solid #E2E8F0" }}>
                                        Done
                                      </span>
                                    </div>
                                    <div className="reminder-note-v2">{rem.note}</div>
                                    <div className="reminder-card-v2-footer">
                                      <div className="reminder-due-v2">
                                        <Check size={12} style={{ color: "#10B981" }} />
                                        <span>Completed ({rem.due_date})</span>
                                      </div>
                                    </div>
                                  </div>
                                );
                              })
                            )}
                          </div>
                        )}
                      </div>
                    </>
                  )}
                </div>
              )}

              {currentView === "settings" && (
                <div className="settings-container">
                  <div className="settings-card">
                    <h2 className="settings-title">Google Sheets Connection Settings</h2>
                    <p className="settings-desc">
                      Configure your Apps Script Web App endpoint URL. The Web App acts as a secure proxy to sync Leads, Deals, and Reminders to your B2B spreadsheets.
                    </p>
                    <form onSubmit={handleSaveApiUrl}>
                      <div className="form-group">
                        <label className="form-label">Apps Script URL</label>
                        <input
                          type="text"
                          className="form-control-input"
                          placeholder="https://script.google.com/macros/s/.../exec"
                          value={apiUrlInput}
                          onChange={(e) => setApiUrlInput(e.target.value)}
                        />
                      </div>
                      <div style={{ display: "flex", gap: "1rem", marginTop: "1.5rem" }}>
                        <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                          Save Config
                        </button>
                        <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={handleTestConnection} disabled={submitting}>
                          {submitting ? "Testing..." : "Test Connection"}
                        </button>
                      </div>
                    </form>

                    {testConnResult && (
                      <div style={{ textAlign: "center" }}>
                        <span className={`settings-badge ${testConnResult === "connected" ? "settings-badge-connected" : "settings-badge-failed"}`}>
                          {testConnResult === "connected" && <CheckCircle size={14} />}
                          {testConnResult === "failed" && <AlertTriangle size={14} />}
                          <span>{testConnResult === "connected" ? "Connected Successfully" : "Connection Failed"}</span>
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </main>

      <div className={`drawer-backdrop ${drawerOpen ? 'open' : ''}`} onClick={() => setDrawerOpen(false)}></div>
      <div className={`drawer ${drawerOpen ? 'open' : ''}`} id="add-lead-drawer">
        <div className="drawer-header">
          <h2 className="drawer-title" id="drawer-title-lbl">
            {drawerType === "lead" && (editingLead ? "Modify Deal details" : "Register New CRM Lead")}
            {drawerType === "deal" && "Open Sales Deal opportunity"}
            {drawerType === "activity" && "Log Sales Touchpoint Activity"}
            {drawerType === "reminder" && "Schedule Client Reminder"}
          </h2>
          <button className="drawer-close" onClick={() => setDrawerOpen(false)} id="btn-close-drawer">
            <X size={20} />
          </button>
        </div>

        {drawerType === "lead" && (
          <form onSubmit={handleLeadSubmit} style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 70px)" }}>
            <div className="drawer-body">
              <div className="form-group">
                <label className="form-label" htmlFor="txt-form-name">Name *</label>
                <input
                  type="text"
                  className="form-control-input"
                  id="txt-form-name"
                  value={leadFormData.name}
                  onChange={(e) => setLeadFormData(prev => ({ ...prev, name: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="txt-form-company">Company *</label>
                <input
                  type="text"
                  className="form-control-input"
                  id="txt-form-company"
                  value={leadFormData.company}
                  onChange={(e) => setLeadFormData(prev => ({ ...prev, company: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="txt-form-email">Email Address *</label>
                <input
                  type="email"
                  className="form-control-input"
                  id="txt-form-email"
                  value={leadFormData.email}
                  onChange={(e) => setLeadFormData(prev => ({ ...prev, email: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="txt-form-phone">Phone Number</label>
                <input
                  type="tel"
                  className="form-control-input"
                  id="txt-form-phone"
                  value={leadFormData.phone}
                  onChange={(e) => setLeadFormData(prev => ({ ...prev, phone: e.target.value }))}
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="txt-form-value">Deal Value (₹)</label>
                <input
                  type="number"
                  className="form-control-input"
                  id="txt-form-value"
                  value={leadFormData.value}
                  onChange={(e) => setLeadFormData(prev => ({ ...prev, value: e.target.value }))}
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="sel-form-source">Lead Acquisition Source</label>
                <select
                  className="form-control-input"
                  id="sel-form-source"
                  value={leadFormData.source}
                  onChange={(e) => setLeadFormData(prev => ({ ...prev, source: e.target.value }))}
                >
                  <option value="Website">Website</option>
                  <option value="Referral">Referral</option>
                  <option value="Cold Outreach">Cold Outreach</option>
                  <option value="LinkedIn">LinkedIn</option>
                  <option value="Partner">Partner</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="sel-form-status">Initial Stage Status</label>
                <select
                  className="form-control-input"
                  id="sel-form-status"
                  value={leadFormData.status}
                  onChange={(e) => setLeadFormData(prev => ({ ...prev, status: e.target.value }))}
                >
                  <option value="New">New</option>
                  <option value="Qualified">Qualified</option>
                  <option value="Proposal">Proposal</option>
                  <option value="Won">Won</option>
                  <option value="Lost">Lost</option>
                </select>
              </div>
            </div>

            <div className="drawer-footer">
              <button type="button" className="btn btn-secondary" onClick={() => setDrawerOpen(false)} id="btn-cancel-submit">Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={submitting} id="btn-confirm-submit">
                {submitting ? (
                  <>
                    <div className="spinner"></div>
                    <span>Saving...</span>
                  </>
                ) : (
                  <span>Save Lead Record</span>
                )}
              </button>
            </div>
          </form>
        )}

        {drawerType === "deal" && (
          <form onSubmit={handleDealSubmit} style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 70px)" }}>
            <div className="drawer-body">
              <div className="form-group">
                <label className="form-label">Deal Title *</label>
                <input
                  type="text"
                  className="form-control-input"
                  placeholder="e.g. Migration Phase 2"
                  value={dealFormData.title}
                  onChange={(e) => setDealFormData(prev => ({ ...prev, title: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Related Contact/Lead *</label>
                <select
                  className="form-control-input"
                  value={dealFormData.lead_id}
                  onChange={(e) => setDealFormData(prev => ({ ...prev, lead_id: e.target.value }))}
                  required
                >
                  {leads.map(l => (
                    <option key={l.id} value={l.id}>{l.name} ({l.company})</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Deal Value (₹) *</label>
                <input
                  type="number"
                  className="form-control-input"
                  value={dealFormData.value}
                  onChange={(e) => setDealFormData(prev => ({ ...prev, value: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Pipeline Stage *</label>
                <select
                  className="form-control-input"
                  value={dealFormData.stage}
                  onChange={(e) => setDealFormData(prev => ({ ...prev, stage: e.target.value }))}
                  required
                >
                  <option value="New">New</option>
                  <option value="Qualified">Qualified</option>
                  <option value="Proposal">Proposal</option>
                  <option value="Won">Won</option>
                  <option value="Lost">Lost</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Target Close Date *</label>
                <input
                  type="date"
                  className="form-control-input"
                  value={dealFormData.close_date}
                  onChange={(e) => setDealFormData(prev => ({ ...prev, close_date: e.target.value }))}
                  required
                />
              </div>
            </div>

            <div className="drawer-footer">
              <button type="button" className="btn btn-secondary" onClick={() => setDrawerOpen(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? (
                  <>
                    <div className="spinner"></div>
                    <span>Creating...</span>
                  </>
                ) : (
                  <span>Insert Deal</span>
                )}
              </button>
            </div>
          </form>
        )}

        {drawerType === "activity" && (
          <form onSubmit={handleActivitySubmit} style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 70px)" }}>
            <div className="drawer-body">
              <div className="form-group">
                <label className="form-label">Select Lead/Contact *</label>
                <select
                  className="form-control-input"
                  value={activityFormData.lead_id}
                  onChange={(e) => setActivityFormData(prev => ({ ...prev, lead_id: e.target.value }))}
                  required
                >
                  {leads.map(l => (
                    <option key={l.id} value={l.id}>{l.name} ({l.company})</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Activity Type *</label>
                <select
                  className="form-control-input"
                  value={activityFormData.type}
                  onChange={(e) => setActivityFormData(prev => ({ ...prev, type: e.target.value }))}
                  required
                >
                  <option value="Call">📞 Phone Call</option>
                  <option value="Email">📧 Email</option>
                  <option value="Meeting">🤝 Business Meeting</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Activity Notes *</label>
                <textarea
                  className="form-control-input"
                  rows={4}
                  placeholder="Summarize the interaction..."
                  value={activityFormData.note}
                  onChange={(e) => setActivityFormData(prev => ({ ...prev, note: e.target.value }))}
                  style={{ resize: "none" }}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Date & Time *</label>
                <input
                  type="datetime-local"
                  className="form-control-input"
                  value={activityFormData.date_time}
                  onChange={(e) => setActivityFormData(prev => ({ ...prev, date_time: e.target.value }))}
                  required
                />
              </div>
            </div>

            <div className="drawer-footer">
              <button type="button" className="btn btn-secondary" onClick={() => setDrawerOpen(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? (
                  <>
                    <div className="spinner"></div>
                    <span>Logging...</span>
                  </>
                ) : (
                  <span>Submit Interaction</span>
                )}
              </button>
            </div>
          </form>
        )}

        {drawerType === "reminder" && (
          <form onSubmit={handleReminderSubmit} style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 70px)" }}>
            <div className="drawer-body">
              <div className="form-group">
                <label className="form-label">Select Lead/Contact *</label>
                <select
                  className="form-control-input"
                  value={reminderFormData.lead_id}
                  onChange={(e) => setReminderFormData(prev => ({ ...prev, lead_id: e.target.value }))}
                  required
                >
                  {leads.map(l => (
                    <option key={l.id} value={l.id}>{l.name} ({l.company})</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Reminder Note *</label>
                <input
                  type="text"
                  className="form-control-input"
                  placeholder="e.g. Discuss security terms and finalize draft contract"
                  value={reminderFormData.note}
                  onChange={(e) => setReminderFormData(prev => ({ ...prev, note: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Due Date *</label>
                <input
                  type="date"
                  className="form-control-input"
                  value={reminderFormData.due_date}
                  onChange={(e) => setReminderFormData(prev => ({ ...prev, due_date: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Priority *</label>
                <select
                  className="form-control-input"
                  value={reminderFormData.priority}
                  onChange={(e) => setReminderFormData(prev => ({ ...prev, priority: e.target.value }))}
                  required
                >
                  <option value="High">High (Red)</option>
                  <option value="Medium">Medium (Amber)</option>
                  <option value="Low">Low (Gray)</option>
                </select>
              </div>
            </div>

            <div className="drawer-footer">
              <button type="button" className="btn btn-secondary" onClick={() => setDrawerOpen(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? (
                  <>
                    <div className="spinner"></div>
                    <span>Saving...</span>
                  </>
                ) : (
                  <span>Save Reminder</span>
                )}
              </button>
            </div>
          </form>
        )}
      </div>

      <div className="toast-container">
        {toasts.map(toast => (
          <div className={`toast ${toast.removing ? 'removing' : ''}`} key={toast.id}>
            <div className="toast-icon">
              {toast.type === "success" && <CheckCircle size={20} className="toast-success-icon" />}
              {toast.type === "error" && <AlertTriangle size={20} className="toast-error-icon" />}
              {toast.type === "info" && <Info size={20} className="toast-info-icon" />}
              {toast.type === "warning" && <AlertTriangle size={20} style={{ color: "#F59E0B" }} />}
            </div>
            <div className="toast-details">
              <div className="toast-title">{toast.title}</div>
              <div className="toast-message">{toast.message}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
