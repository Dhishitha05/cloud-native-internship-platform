const API_BASE_URL = "http://127.0.0.1:5000/api";

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("internmatch_token");

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      data.error || data.message || `Request failed: ${response.status}`
    );
  }

  return data;
}

export async function registerUser({
  name,
  email,
  password,
  role,
  company_name,
}) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify({
      name,
      email,
      password,
      role: role.toUpperCase(),
      ...(company_name ? { company_name } : {}),
    }),
  });
}

export async function loginUser({ email, password }) {
  const data = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  localStorage.setItem("internmatch_token", data.access_token);
  localStorage.setItem("internmatch_user", JSON.stringify(data.user));

  return data;
}

export async function getCurrentUser() {
  return apiRequest("/auth/me");
}

export async function getInternships() {
  return apiRequest("/internships/");
}

export function logoutUser() {
  localStorage.removeItem("internmatch_token");
  localStorage.removeItem("internmatch_user");
}

export async function applyForInternship(internshipId, coverLetter = "") {
  return apiRequest("/applications/", {
    method: "POST",
    body: JSON.stringify({
      internship_id: Number(internshipId),
      cover_letter: coverLetter,
    }),
  });
}

export async function getMyApplications() {
  return apiRequest("/applications/my");
}


export async function createInternship(internship) {
  return apiRequest("/internships/", {
    method: "POST",
    body: JSON.stringify(internship),
  });
}