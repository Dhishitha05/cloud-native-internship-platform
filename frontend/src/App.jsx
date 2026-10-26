import React, { useEffect, useMemo, useState } from "react";
import {
  ArrowRight, BriefcaseBusiness, Building2, CheckCircle2, ChevronRight,
  Clock3, Filter, GraduationCap, LayoutDashboard, LogIn, Menu, Search,
  Settings, ShieldCheck, Sparkles, Target, TrendingUp, Users, X, Plus,
  MapPin, Bookmark, Bell, FileText, Eye, Edit3, Trash2
} from "lucide-react";
import { Link, NavLink, Route, Routes, useLocation, useNavigate, useParams } from "react-router-dom";
import { internships, applications } from "./data";
import {
  registerUser,
  loginUser,
  getInternships,
  applyForInternship,
  getMyApplications,
  createInternship
} from "./api";
function useLiveInternships() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getInternships()
      .then((data) => {
        const list = Array.isArray(data) ? data : data.internships || [];

        setItems(list.map((item) => ({
          ...item,
          company: item.company || item.company_name || "Hiring company",
          location: item.location || "Location not specified",
          duration: item.duration_months
            ? `${item.duration_months} months`
            : "Not specified",
          stipend: item.stipend != null
            ? `₹${item.stipend}`
            : "Not specified",
          type: item.type || "Not specified",
          skills: Array.isArray(item.skills) ? item.skills : [],
          logo: (item.company || item.company_name || item.title || "IN")
            .slice(0, 2)
            .toUpperCase(),
          posted: item.created_at
            ? new Date(item.created_at).toLocaleDateString()
            : "Recently"
        })));
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { items, loading, error };
}

const navItems = [
  ["Dashboard", "/student", LayoutDashboard],
  ["Internships", "/internships", BriefcaseBusiness],
  ["Applications", "/applications", FileText],
  ["My Skills", "/skills", Target]
];

function Logo() {
  return <Link to="/" className="logo"><span className="logo-mark">I</span><span>Intern<span className="accent">Match</span></span></Link>;
}

function Landing() {
  return (
    <div className="landing">
      <header className="landing-nav container">
        <Logo />
        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how">How it works</a>
          <Link to="/internships">Explore internships</Link>
        </div>
        <div className="nav-actions">
          <Link className="btn btn-ghost" to="/login">Log in</Link>
          <Link className="btn btn-primary" to="/register">Get started <ArrowRight size={17}/></Link>
        </div>
      </header>

      <main>
        <section className="hero container">
          <div className="hero-copy">
            <div className="eyebrow"><Sparkles size={15}/> Smarter internship matching</div>
            <h1>Find the internship that <span className="gradient-text">fits you.</span></h1>
            <p>InternMatch connects students with internships based on their skills, interests and career goals — not just keywords.</p>
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-lg">Start matching <ArrowRight size={18}/></Link>
              <Link to="/internships" className="btn btn-secondary btn-lg">Browse internships</Link>
            </div>
            <div className="trust-row">
              <div><strong>1,200+</strong><span>Internships</span></div>
              <div><strong>450+</strong><span>Companies</span></div>
              <div><strong>92%</strong><span>Avg. match accuracy</span></div>
            </div>
          </div>
          <div className="hero-visual">
            <div className="dashboard-preview">
              <div className="preview-top"><div className="mini-dots">•••</div><span>Student Dashboard</span><Bell size={16}/></div>
              <div className="preview-welcome">Good morning, Dhishitha 👋<small>Your perfect internship could be one search away.</small></div>
              <div className="preview-stats">
                <div><span>Applications</span><b>12</b><em>+3 this week</em></div>
                <div><span>Avg. Match</span><b>89%</b><em>↑ 6%</em></div>
              </div>
              <div className="preview-match">
                <div className="match-head"><div><span>Top match for you</span><b>Frontend Developer Intern</b></div><strong>96%</strong></div>
                <div className="company-line"><span className="company-avatar">TN</span> TechNova Labs <span>· Hyderabad</span></div>
                <div className="skill-row"><span>React</span><span>JavaScript</span><span>CSS</span><span>HTML</span></div>
              </div>
              <div className="floating-card"><CheckCircle2 size={18}/><div><b>Great match!</b><small>4/4 core skills matched</small></div></div>
            </div>
          </div>
        </section>

        <section id="features" className="section container">
          <div className="section-heading"><span className="eyebrow">WHY INTERNMATCH</span><h2>Everything you need to land the right internship.</h2><p>From discovery to application tracking, InternMatch keeps your entire internship journey in one place.</p></div>
          <div className="feature-grid">
            <Feature icon={Target} title="Skill-based matching" text="See a clear match percentage for every internship based on your actual skills." />
            <Feature icon={Search} title="Smart discovery" text="Search and filter opportunities by role, location, stipend, skills and type." />
            <Feature icon={TrendingUp} title="Track applications" text="Know exactly where each application stands from applied to interview." />
            <Feature icon={Building2} title="Employer tools" text="Companies can post roles, review applicants and find the strongest matches." />
          </div>
        </section>

        <section id="how" className="section soft-bg">
          <div className="container">
            <div className="section-heading"><span className="eyebrow">HOW IT WORKS</span><h2>From skills to opportunity in four steps.</h2></div>
            <div className="steps">
              {[
                ["01","Create your profile","Add your education, skills and career interests."],
                ["02","Discover matches","Browse internships ranked by skill compatibility."],
                ["03","Apply with confidence","Review requirements and submit your application."],
                ["04","Track your progress","Follow applications and interview stages in one dashboard."]
              ].map(([n,t,d]) => <div className="step" key={n}><span>{n}</span><h3>{t}</h3><p>{d}</p></div>)}
            </div>
          </div>
        </section>
      </main>
      <footer className="footer container"><Logo/><span>© 2026 InternMatch. Built for students and employers.</span></footer>
    </div>
  );
}

function Feature({icon: Icon, title, text}) {
  return <div className="feature-card"><div className="icon-box"><Icon size={21}/></div><h3>{title}</h3><p>{text}</p><ChevronRight className="feature-arrow" size={18}/></div>;
}

function Auth({ mode = "login" }) {
  const isLogin = mode === "login";
  const navigate = useNavigate();

  const [role, setRole] = useState("student");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    const name = formData.get("name")?.trim();
    const companyName = formData.get("companyName")?.trim();
    const email = formData.get("email")?.trim();
    const password = formData.get("password");

    try {
        if (isLogin) {
          const data = await loginUser({ email, password });

          const userRole = data.user.role.toLowerCase();
          navigate(userRole === "employer" ? "/employer" : "/student");
        } else {
          if (role === "employer" && !companyName) {
            throw new Error("Please enter your company name.");
          }

          const registrationData = {
            name,
            email,
            password,
            role,
            ...(role === "employer" ? { company_name: companyName } : {}),
          };

          await registerUser(registrationData);

          const data = await loginUser({ email, password });

          const userRole = data.user.role.toLowerCase();
          navigate(userRole === "employer" ? "/employer" : "/student");
        }

    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-left">
        <Logo />
        <div className="auth-message">
          <div className="eyebrow"><Sparkles size={15} /> InternMatch</div>
          <h1>Build your next career move.</h1>
          <p>Discover opportunities matched to your skills and goals.</p>
          <div className="auth-points">
            <span><CheckCircle2 size={17} /> Skill-based recommendations</span>
            <span><CheckCircle2 size={17} /> Simple application tracking</span>
            <span><CheckCircle2 size={17} /> Opportunities from growing companies</span>
          </div>
        </div>
      </div>

      <div className="auth-card-wrap">
        <form className="auth-card" onSubmit={submit}>
          <Link to="/" className="mobile-logo"><Logo /></Link>

          <h2>{isLogin ? "Welcome back" : "Create your account"}</h2>
          <p>
            {isLogin
              ? "Sign in to continue to your dashboard."
              : "Join InternMatch and find your best-fit internship."}
          </p>

          {!isLogin && (
            <div className="role-toggle">
              <button
                type="button"
                className={role === "student" ? "active" : ""}
                onClick={() => setRole("student")}
              >
                <GraduationCap size={17} /> Student
              </button>
              <button
                type="button"
                className={role === "employer" ? "active" : ""}
                onClick={() => setRole("employer")}
              >
                <Building2 size={17} /> Employer
              </button>
            </div>
          )}

          {!isLogin && (
            <label>
              Full name
              <input
                name="name"
                required
                placeholder="Enter your name"
                autoComplete="name"
              />
            </label>
          )}
          {!isLogin && role === "employer" && (
            <label>
              Company name
              <input
                name="companyName"
                required
                placeholder="Enter your company name"
                autoComplete="organization"
              />
            </label>
          )}

          <label>
            Email address
            <input
              name="email"
              required
              type="email"
              placeholder="you@example.com"
              autoComplete="email"
            />
          </label>

          <label>
            Password
            <input
              name="password"
              required
              type="password"
              placeholder="Enter your password"
              autoComplete={isLogin ? "current-password" : "new-password"}
            />
          </label>

          {isLogin && (
            <div className="form-row">
              <label className="checkbox">
                <input type="checkbox" /> Remember me
              </label>
              <a href="#forgot">Forgot password?</a>
            </div>
          )}

          {error && (
            <p role="alert" style={{ color: "#dc2626" }}>
              {error}
            </p>
          )}

          <button
            className="btn btn-primary full"
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Please wait..."
              : isLogin
                ? "Sign in"
                : "Create account"}
            {!loading && <ArrowRight size={17} />}
          </button>

          <div className="divider"><span>or</span></div>
          <button type="button" className="social-btn" disabled>
            Google sign-in unavailable
          </button>

          <p className="auth-switch">
            {isLogin
              ? "Don't have an account?"
              : "Already have an account?"}{" "}
            <Link to={isLogin ? "/register" : "/login"}>
              {isLogin ? "Create one" : "Sign in"}
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
function AppShell({children, employer=false}) {
  const [open, setOpen] = useState(false);
  const location = useLocation();
  const savedUser = JSON.parse(
    localStorage.getItem("internmatch_user") || "{}"
  );

  const userName = savedUser.name || (employer ? "Employer" : "Student");
  const initials = userName
    .split(" ")
    .filter(Boolean)
    .map(part => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
  const items = employer ? [["Dashboard","/employer",LayoutDashboard],["Post Internship","/employer/post",Plus],["Internships","/employer/internships",BriefcaseBusiness],["Applicants","/employer/applicants",Users]] : navItems;
  return <div className="app-shell">
    <aside className={open?"sidebar open":"sidebar"}>
      <div className="side-logo"><Logo/><button className="close-side" onClick={()=>setOpen(false)}><X size={19}/></button></div>
      <div className="side-role">{employer?<><Building2 size={14}/> EMPLOYER PORTAL</>:<><GraduationCap size={14}/> STUDENT PORTAL</>}</div>
      <nav>{items.map(([name,path,Icon]) => <NavLink key={path} to={path} className={({isActive})=>isActive||location.pathname===path?"active":""} onClick={()=>setOpen(false)}><Icon size={18}/><span>{name}</span></NavLink>)}</nav>
      <div className="sidebar-bottom"><NavLink to="/settings"><Settings size={18}/> Settings</NavLink><Link to="/" onClick={()=>localStorage.clear()}><LogIn size={18}/> Sign out</Link></div>
    </aside>
    <div className="main-area">
      <header className="topbar"><button className="menu-btn" onClick={()=>setOpen(true)}><Menu/></button><div className="top-search"><Search size={17}/><input placeholder="Search internships, skills, companies..." /></div><div className="top-actions"><button className="circle-btn"><Bell size={18}/><i/></button><div className="user-chip"><span>{initials}</span><div><b>{userName}</b><small>{employer?"Employer":"Student"}</small></div></div></div></header>
      <main className="content">{children}</main>
    </div>
  </div>;
}

function Stat({label,value,change,icon:Icon}) {
  return <div className="stat-card"><div className="stat-icon"><Icon size={19}/></div><div><span>{label}</span><strong>{value}</strong><small className={change?.startsWith("+")?"positive":""}>{change}</small></div></div>;
}

function MatchCard({item}) {
  return <div className="match-card">
    <div className="match-card-top"><span className="company-avatar">{item.logo}</span><button className="bookmark"><Bookmark size={17}/></button></div>
    <div className="match-percent">
      <b>{item.match != null ? `${item.match}%` : "—"}</b>
      <span>{item.match != null ? "match" : "skill match pending"}</span>
    </div>
    <h3>{item.title}</h3><p className="company-name">{item.company}</p>
    <p className="muted"><MapPin size={14}/> {item.location}</p>
    <div className="skill-row">{item.skills.slice(0,3).map(s=><span key={s}>{s}</span>)}</div>
    <Link to={`/internships/${item.id}`} className="card-link">View details <ArrowRight size={16}/></Link>
  </div>;
}


function StudentDashboard() {
  const savedUser = JSON.parse(
    localStorage.getItem("internmatch_user") || "{}"
  );
  const name = savedUser.name || "Student";

  return <AppShell>
    <div className="page-header">
      <div>
        <span className="eyebrow">STUDENT DASHBOARD</span>
        <h1>Good morning, {name} 👋</h1>
        <p>Here’s what’s happening with your internship search.</p>
      </div>
      <Link className="btn btn-primary" to="/internships">
        <Search size={17}/> Find internships
      </Link>
    </div>

    <div className="stats-grid">
      <Stat label="Applications" value="12" change="+3 this week" icon={FileText}/>
      <Stat label="Avg. match score" value="89%" change="+6% this month" icon={Target}/>
      <Stat label="Profile views" value="48" change="+12 this week" icon={Eye}/>
      <Stat label="Interviews" value="3" change="+1 this week" icon={BriefcaseBusiness}/>
    </div>

    <div className="section-row">
      <div>
        <h2>Top matches for you</h2>
        <p>Internships ranked by your current skill profile.</p>
      </div>
      <Link to="/internships" className="text-link">View all <ArrowRight size={15}/></Link>
    </div>

    <div className="match-grid">
      {internships.slice(0,3).map(i => <MatchCard key={i.id} item={i}/>)}
    </div>

    <div className="lower-grid">
      <div className="panel">
        <div className="panel-title">
          <div><h2>Recent applications</h2><p>Your latest application activity.</p></div>
          <Link to="/applications">View all</Link>
        </div>
        {applications.map(a => (
          <div className="application-row" key={a.id}>
            <div className="company-avatar small">{a.company.slice(0,2).toUpperCase()}</div>
            <div className="application-main">
              <b>{a.role}</b><span>{a.company} · Applied {a.date}</span>
            </div>
            <span className={`status ${a.status.toLowerCase().replaceAll(" ","-")}`}>{a.status}</span>
          </div>
        ))}
      </div>

      <div className="panel profile-progress">
        <div className="panel-title">
          <div><h2>Profile strength</h2><p>Complete your profile to improve matches.</p></div>
          <strong>82%</strong>
        </div>
        <div className="progress"><span style={{width:"82%"}}/></div>
        <div className="check-list">
          <span><CheckCircle2 size={16}/> Basic information</span>
          <span><CheckCircle2 size={16}/> Education</span>
          <span><CheckCircle2 size={16}/> Skills</span>
          <span className="todo"><Clock3 size={16}/> Add resume</span>
        </div>
        <Link className="btn btn-secondary full" to="/skills">Complete profile</Link>
      </div>
    </div>
  </AppShell>;
}


function InternshipList() {
  const { items, loading, error } = useLiveInternships();
  const [query,setQuery] = useState("");
  const [skill,setSkill] = useState("All skills");
  const [sort,setSort] = useState("Best match");
  const allSkills = ["All skills", ...new Set(items.flatMap(i => i.skills))];
  const results = useMemo(() => {
    return items
      .filter((item) =>
        `${item.title} ${item.company} ${item.location} ${item.skills.join(" ")}`
          .toLowerCase()
          .includes(query.toLowerCase()) &&
        (skill === "All skills" || item.skills.includes(skill))
      )
      .sort((a, b) =>
        sort === "Alphabetical"
          ? a.title.localeCompare(b.title)
          : a.title.localeCompare(b.title)
      );
  }, [items, query, skill, sort]);
  return <AppShell>
    <div className="page-header"><div><span className="eyebrow">OPPORTUNITIES</span><h1>Find your next internship</h1><p>Explore opportunities matched to your skills and interests.</p></div></div>
    <div className="search-panel"><div className="big-search"><Search size={19}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search by role, company or skill..." /></div><div className="filter"><Filter size={17}/><select value={skill} onChange={e=>setSkill(e.target.value)}>{allSkills.map(s=><option key={s}>{s}</option>)}</select></div><select className="sort-select" value={sort} onChange={e=>setSort(e.target.value)}><option>Best match</option><option>Alphabetical</option></select></div>
    {loading && <p>Loading internships...</p>}
    {error && (
      <p role="alert">
        Could not load internships: {error}
      </p>
    )}

    {!loading && !error && results.length === 0 && (
      <p>
        No internships found. Try a different search or ask an employer to post one.
      </p>
    )}
    <div className="results-head"><span><b>{results.length}</b> internships found</span><span className="muted">Updated today</span></div>
    <div className="internship-list">{results.map(i=><div className="internship-card" key={i.id}><span className="company-avatar">{i.logo}</span><div className="internship-info"><div className="internship-title"><h3>{i.title}</h3><span className="match-badge">
  {i.match != null ? `${i.match}% match` : "Match pending"}
</span></div><b className="company-name">{i.company}</b><div className="meta"><span><MapPin size={14}/>{i.location}</span><span><Clock3 size={14}/>{i.duration}</span><span><BriefcaseBusiness size={14}/>{i.stipend}</span></div><div className="skill-row">{i.skills.map(s=><span key={s}>{s}</span>)}</div></div><Link to={`/internships/${i.id}`} className="btn btn-secondary">View internship</Link></div>)}</div>
  </AppShell>;
}


function InternshipDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { items, loading, error } = useLiveInternships();
  const [applied, setApplied] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [applyError, setApplyError] = useState("");

  const item = items.find((x) => Number(x.id) === Number(id));

  async function handleApply() {
    setSubmitting(true);
    setApplyError("");

    try {
      await applyForInternship(id);
      setApplied(true);
    } catch (err) {
      setApplyError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <AppShell><p>Loading internship details...</p></AppShell>;
  }

  if (error || !item) {
    return (
      <AppShell>
        <p>{error || "Internship not found."}</p>
        <Link to="/internships">Back to internships</Link>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <Link to="/internships" className="back-link">
        ← Back to internships
      </Link>

      <div className="detail-layout">
        <article className="detail-main">
          <div className="detail-company">
            <span className="company-avatar large">{item.logo}</span>
            <div>
              <span className="eyebrow">{item.company}</span>
              <h1>{item.title}</h1>
              <p><MapPin size={15} /> {item.location}</p>
            </div>
          </div>

          <div className="detail-section">
            <h2>About the internship</h2>
            <p>{item.description}</p>
          </div>

          <div className="detail-section">
            <h2>Required skills</h2>
            {item.skills.length > 0
              ? <div className="detail-skills">
                  {item.skills.map((skill) => (
                    <span key={skill}><CheckCircle2 size={15} />{skill}</span>
                  ))}
                </div>
              : <p>Skills information is not available yet.</p>
            }
          </div>
        </article>

        <aside className="detail-side">
          <div className="apply-card">
            <h3>{item.title}</h3>
            <p className="company-name">{item.company}</p>

            <div className="detail-facts">
              <span><b>Stipend</b>{item.stipend}</span>
              <span><b>Duration</b>{item.duration}</span>
              <span><b>Location</b>{item.location}</span>
            </div>

            <button
              className="btn btn-primary full"
              onClick={handleApply}
              disabled={applied || submitting}
            >
              {applied
                ? "Application submitted"
                : submitting
                  ? "Submitting..."
                  : "Apply now"}
            </button>

            {applyError && (
              <p role="alert">{applyError}</p>
            )}

            {applied && (
              <div className="success-box">
                Your application has been saved successfully.
              </div>
            )}
          </div>
        </aside>
      </div>
    </AppShell>
  );
}



function Applications() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getMyApplications()
      .then((data) => {
        setItems(Array.isArray(data) ? data : []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const formatDate = (value) => {
    if (!value) return "Date unavailable";
    return new Date(value).toLocaleDateString();
  };

  const statusLabel = (value) =>
    value ? value.replaceAll("_", " ") : "Applied";

  return (
    <AppShell>
      <div className="page-header">
        <div>
          <span className="eyebrow">APPLICATIONS</span>
          <h1>Application tracking</h1>
          <p>Keep track of every opportunity you’ve applied to.</p>
        </div>
      </div>

      {loading && <p>Loading your applications...</p>}

      {error && (
        <p role="alert">Could not load applications: {error}</p>
      )}

      {!loading && !error && items.length === 0 && (
        <div className="panel">
          You haven't applied for any internships yet.
        </div>
      )}

      {!loading && !error && items.length > 0 && (
        <div className="panel">
          <div className="table-head">
            <span>Internship</span>
            <span>Applied</span>
            <span>Status</span>
          </div>

          {items.map((item) => (
            <div className="application-table-row" key={item.id}>
              <div>
                <b>{item.internship_title}</b>
                <span>{item.domain || item.location || "Internship"}</span>
              </div>

              <span>{formatDate(item.applied_at)}</span>

              <span
                className={`status ${statusLabel(item.status)
                  .toLowerCase()
                  .replaceAll(" ", "-")}`}
              >
                {statusLabel(item.status)}
              </span>
            </div>
          ))}
        </div>
      )}
    </AppShell>
  );
}


function Skills() {
  const [skills,setSkills]=useState(["React","JavaScript","Python","MySQL","AWS","Docker"]);
  const [input,setInput]=useState("");
  const add=()=>{if(input.trim()&&!skills.includes(input.trim())) setSkills([...skills,input.trim()]);setInput("")};
  return <AppShell><div className="page-header"><div><span className="eyebrow">PROFILE</span><h1>My skills</h1><p>Keep your skills updated to improve internship matches.</p></div></div><div className="skills-layout"><div className="panel"><h2>Your skills</h2><p className="muted">Add technologies and skills you can confidently work with.</p><div className="skill-editor">{skills.map(s=><span key={s}>{s}<button onClick={()=>setSkills(skills.filter(x=>x!==s))}>×</button></span>)}</div><div className="add-skill"><input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter"&&add()} placeholder="Type a skill..." /><button className="btn btn-primary" onClick={add}><Plus size={17}/> Add skill</button></div></div><div className="panel"><div className="match-score-big"><div><span>Profile match score</span><strong>89%</strong></div><Target size={42}/></div><p>Strong profiles get more relevant recommendations and better visibility to employers.</p><Link to="/internships" className="btn btn-secondary full">See matched internships</Link></div></div></AppShell>;
}


function EmployerDashboard() {
  const savedUser = JSON.parse(
    localStorage.getItem("internmatch_user") || "{}"
  );
  const name = savedUser.name || "Employer";

  return (
    <AppShell employer>
      <div className="page-header">
        <div>
          <span className="eyebrow">EMPLOYER DASHBOARD</span>
          <h1>Good morning, {name} 👋</h1>
          <p>Here’s an overview of your internship hiring activity.</p>
        </div>
        <Link className="btn btn-primary" to="/employer/post">
          <Plus size={17} /> Post internship
        </Link>
      </div>

      <div className="stats-grid">
        <Stat label="Active internships" value="8" change="+2 this month" icon={BriefcaseBusiness} />
        <Stat label="Total applicants" value="284" change="+18% this month" icon={Users} />
        <Stat label="Shortlisted" value="42" change="+7 this week" icon={CheckCircle2} />
        <Stat label="Interviews" value="16" change="+3 this week" icon={FileText} />
      </div>

      <div className="lower-grid">
        <div className="panel">
          <div className="panel-title">
            <div>
              <h2>Recent applicants</h2>
              <p>Applicants across your active roles.</p>
            </div>
            <Link to="/employer/applicants">View all</Link>
          </div>

          {["Aarav Sharma", "Meera Reddy", "Rohan Kumar", "Ananya Rao"].map((n, i) => (
            <div className="application-row" key={n}>
              <span className="person-avatar">
                {n.split(" ").map(x => x[0]).join("")}
              </span>
              <div className="application-main">
                <b>{n}</b>
                <span>
                  {["Frontend Developer", "Cloud & DevOps", "Python Backend", "Java Developer"][i]}
                  {" · "}{94 - i * 5}% match
                </span>
              </div>
              <button className="icon-action">
                <Eye size={17} />
              </button>
            </div>
          ))}
        </div>

        <div className="panel">
          <div className="panel-title">
            <div>
              <h2>Active internships</h2>
              <p>Your current open roles.</p>
            </div>
          </div>

          {internships.slice(0, 4).map(i => (
            <div className="compact-role" key={i.id}>
              <span className="company-avatar small">TN</span>
              <div>
                <b>{i.title}</b>
                <span>{i.location}</span>
              </div>
              <strong>{28 - i.id * 2} applicants</strong>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}



function PostInternship() {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [posted, setPosted] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const form = new FormData(e.currentTarget);
    const stipendValue = form.get("stipend");
    const durationValue = form.get("duration_months");

    const internship = {
      title: form.get("title").trim(),
      domain: form.get("domain").trim(),
      location: form.get("location").trim(),
      duration_months: Number(durationValue),
      stipend: stipendValue ? Number(stipendValue) : null,
      description: form.get("description").trim(),
      eligibility: form.get("eligibility").trim() || null,
    };

    if (
      !internship.title ||
      !internship.domain ||
      !internship.description
    ) {
      setError("Please fill in the required fields.");
      return;
    }

    if (
      internship.stipend !== null &&
      (!Number.isFinite(internship.stipend) || internship.stipend < 0)
    ) {
      setError("Please enter a valid stipend amount.");
      return;
    }

    setSubmitting(true);

    try {
      await createInternship(internship);
      setPosted(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AppShell employer>
      <div className="page-header">
        <div>
          <span className="eyebrow">EMPLOYER PORTAL</span>
          <h1>Post an internship</h1>
          <p>Create a clear role so the right students can find it.</p>
        </div>
      </div>

      {posted ? (
        <div className="success-panel">
          <CheckCircle2 size={45} />
          <h2>Internship posted successfully!</h2>
          <p>Your internship has been saved and is available in the listings.</p>
          <button
            className="btn btn-primary"
            onClick={() => navigate("/internships")}
          >
            View internships
          </button>
        </div>
      ) : (
        <form className="form-panel" onSubmit={handleSubmit}>
          <div className="form-section">
            <h2>Basic information</h2>

            <div className="form-grid">
              <label>
                Internship title
                <input
                  name="title"
                  required
                  placeholder="e.g. Frontend Developer Intern"
                />
              </label>

              <label>
                Domain
                <input
                  name="domain"
                  required
                  placeholder="e.g. Engineering"
                />
              </label>

              <label>
                Location
                <input
                  name="location"
                  placeholder="e.g. Hyderabad / Remote"
                />
              </label>

              <label>
                Duration
                <select name="duration_months" defaultValue="3">
                  <option value="3">3 months</option>
                  <option value="4">4 months</option>
                  <option value="6">6 months</option>
                  <option value="12">12 months</option>
                </select>
              </label>

              <label>
                Monthly stipend (₹)
                <input
                  name="stipend"
                  type="number"
                  min="0"
                  placeholder="e.g. 20000"
                />
              </label>

              <label>
                Eligibility
                <input
                  name="eligibility"
                  placeholder="e.g. B.Tech students"
                />
              </label>
            </div>
          </div>

          <div className="form-section">
            <h2>Skills & description</h2>
            <label>
              Internship description
              <textarea
                name="description"
                required
                rows="6"
                placeholder="Describe responsibilities and requirements..."
              />
            </label>
          </div>

          {error && <p role="alert">{error}</p>}

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate("/employer")}
            >
              Cancel
            </button>
            <button
              className="btn btn-primary"
              disabled={submitting}
            >
              {submitting ? "Publishing..." : "Publish internship"}
              <ArrowRight size={17} />
            </button>
          </div>
        </form>
      )}
    </AppShell>
  );
}


function EmployerInternships() {
  return <AppShell employer><div className="page-header"><div><span className="eyebrow">MANAGE ROLES</span><h1>Your internships</h1><p>Manage open and closed internship opportunities.</p></div><Link className="btn btn-primary" to="/employer/post"><Plus size={17}/> Post internship</Link></div><div className="panel"><div className="table-head"><span>Role</span><span>Location</span><span>Applicants</span><span>Status</span></div>{internships.slice(0,5).map((i,idx)=><div className="application-table-row" key={i.id}><div><b>{i.title}</b><span>Posted {i.posted}</span></div><span>{i.location}</span><span>{28-idx*4}</span><span className="status interview">Active</span></div>)}</div></AppShell>;
}

function Applicants() {
  const applicants=[["Aarav Sharma","Frontend Developer Intern","94%","Interview"],["Meera Reddy","Cloud & DevOps Intern","89%","Shortlisted"],["Rohan Kumar","Python Backend Intern","86%","Under Review"],["Ananya Rao","Java Developer Intern","82%","Applied"],["Kiran Patel","Frontend Developer Intern","78%","Applied"]];
  return <AppShell employer><div className="page-header"><div><span className="eyebrow">APPLICANT MANAGEMENT</span><h1>Applicants</h1><p>Review candidates ranked by skill compatibility.</p></div></div><div className="search-panel"><div className="big-search"><Search size={19}/><input placeholder="Search applicants or internships..." /></div><select className="sort-select"><option>All statuses</option><option>Shortlisted</option><option>Interview</option></select></div><div className="panel"><div className="table-head applicant-head"><span>Candidate</span><span>Internship</span><span>Match</span><span>Status</span><span>Action</span></div>{applicants.map(([name,role,match,status])=><div className="application-table-row applicant-row" key={name}><div className="person-cell"><span className="person-avatar">{name.split(" ").map(x=>x[0]).join("")}</span><b>{name}</b></div><span>{role}</span><strong className="match-text">{match}</strong><span className="status interview">{status}</span><button className="btn btn-secondary btn-small"><Eye size={15}/> Review</button></div>)}</div></AppShell>;
}

function SettingsPage() { return <AppShell><div className="page-header"><div><span className="eyebrow">ACCOUNT</span><h1>Settings</h1><p>Manage your account preferences.</p></div></div><div className="panel settings-panel"><h2>Notifications</h2><label className="setting-row"><span><b>Internship recommendations</b><small>Receive weekly recommendations based on your skills.</small></span><input type="checkbox" defaultChecked/></label><label className="setting-row"><span><b>Application updates</b><small>Get notified when an application status changes.</small></span><input type="checkbox" defaultChecked/></label><h2>Privacy</h2><label className="setting-row"><span><b>Employer profile visibility</b><small>Allow employers to discover your profile for relevant roles.</small></span><input type="checkbox" defaultChecked/></label></div></AppShell> }

export default function App() {
  return <Routes>
    <Route path="/" element={<Landing/>}/>
    <Route path="/login" element={<Auth mode="login"/>}/>
    <Route path="/register" element={<Auth mode="register"/>}/>
    <Route path="/student" element={<StudentDashboard/>}/>
    <Route path="/internships" element={<InternshipList/>}/>
    <Route path="/internships/:id" element={<InternshipDetail/>}/>
    <Route path="/applications" element={<Applications/>}/>
    <Route path="/skills" element={<Skills/>}/>
    <Route path="/settings" element={<SettingsPage/>}/>
    <Route path="/employer" element={<EmployerDashboard/>}/>
    <Route path="/employer/post" element={<PostInternship/>}/>
    <Route path="/employer/internships" element={<EmployerInternships/>}/>
    <Route path="/employer/applicants" element={<Applicants/>}/>
  </Routes>;
}