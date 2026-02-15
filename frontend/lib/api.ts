import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export interface RegisterData {
  full_name: string;
  cnic: string;
  mobile: string;
  email: string;
  username: string;
  password: string;
}

export interface ShopRegisterData extends RegisterData {
  shop_license_number: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface UserInfo {
  id: number;
  username: string;
  full_name: string;
  role: string;
  is_shop_verified?: boolean;
}

export interface MobileDevice {
  id: number;
  imei: string;
  mobile_number: string;
  brand: string | null;
  model: string | null;
  current_owner_cnic: string;
  registered_by_user_id: number;
  registration_type: string;
  status: string;
  invoice_path: string | null;
  registration_date: string;
  updated_at: string;
  notes: string | null;
}

export interface TransferRecord {
  id: number;
  mobile_id: number;
  imei: string;
  old_owner_cnic: string;
  new_owner_cnic: string;
  transferred_by_user_id: number;
  transfer_type: string;
  transfer_date: string;
  notes: string | null;
}

export interface AuditLogEntry {
  id: number;
  user_id: number | null;
  action_type: string;
  entity_type: string | null;
  entity_id: number | null;
  description: string;
  extra_data: Record<string, unknown> | null;
  ip_address: string | null;
  created_at: string;
}

export interface DeviceStats {
  owned_devices: number;
  registered_devices: number;
  stolen_devices: number;
}

export interface AdminStats {
  total_users: number;
  total_devices: number;
  total_shop_keepers: number;
  pending_shop_approvals: number;
  blocked_devices: number;
  unreviewed_alerts: number;
  unreviewed_snatch_reports: number;
}

export interface InitiateTransferResponse {
  message: string;
  old_owner_cnic: string;
  old_owner_name: string;
  device_brand: string | null;
  device_model: string | null;
}

export interface VerifyOldOwnerResponse {
  message: string;
  verified: boolean;
}

export interface SendNewOwnerOTPResponse {
  message: string;
  new_owner_cnic: string;
  new_owner_name: string;
}

export interface CompleteTransferResponse {
  message: string;
  imei: string;
  old_owner_cnic: string;
  new_owner_cnic: string;
  transfer_type: string;
}

export interface SnatchReport {
  id: number;
  reporter_user_id: number;
  reporter_cnic: string;
  reporter_name: string;
  reporter_phone: string;
  victim_cnic: string;
  device_imei: string;
  mobile_id: number | null;
  incident_description: string;
  incident_date: string | null;
  incident_location: string | null;
  status: string;
  is_reviewed: boolean;
  reviewed_by_user_id: number | null;
  reviewed_at: string | null;
  admin_notes: string | null;
  created_at: string;
}

export interface CitizenReportStats {
  total_owned: number;
  total_transferred_away: number;
  total_received: number;
}

export interface ShopReportStats {
  total_registered: number;
  total_transferred: number;
}

export interface DeviceCheckResult {
  found: boolean;
  status: string;
  brand?: string | null;
  model?: string | null;
  registration_date?: string | null;
  message?: string | null;
  is_owner?: boolean;
}

export interface PoliceAlertRecord {
  id: number;
  imei: string;
  mobile_id: number | null;
  checker_user_id: number;
  checker_cnic: string;
  checker_name: string;
  checker_phone: string;
  checker_role: string;
  device_status: string;
  ip_address: string | null;
  user_agent: string | null;
  is_reviewed: boolean;
  created_at: string;
}

export const authApi = {
  register: (data: RegisterData) => api.post("/auth/register", data),
  registerShop: (data: ShopRegisterData) => api.post("/auth/register-shop", data),
  login: (data: LoginData) => api.post("/auth/login", data),
  logout: () => api.post("/auth/logout"),
  verify: () => api.get("/auth/verify"),
};

export const userApi = {
  getProfile: () => api.get("/user/profile"),
  updateProfile: (data: Partial<{ full_name: string; email: string; mobile: string }>) =>
    api.put("/user/profile", null, { params: data }),
};

export const mobileApi = {
  registerSelf: (data: { imei: string; mobile_number: string; brand?: string; model?: string; notes?: string }) =>
    api.post("/mobiles/register-self", data),
  registerShop: (data: { imei: string; mobile_number: string; brand?: string; model?: string; customer_cnic: string; notes?: string }) =>
    api.post("/mobiles/register-shop", data),
  list: () => api.get<MobileDevice[]>("/mobiles"),
  getById: (id: number) => api.get<MobileDevice>(`/mobiles/${id}`),
  getByImei: (imei: string) => api.get<MobileDevice>(`/mobiles/by-imei/${imei}`),
  getStats: () => api.get<DeviceStats>("/mobiles/stats"),
};

export const transferApi = {
  list: () => api.get<TransferRecord[]>("/transfers"),
  getById: (id: number) => api.get<TransferRecord>(`/transfers/${id}`),
};

export const deviceCheckApi = {
  check: (imei: string) => api.post<DeviceCheckResult>("/device-check", { imei }),
  transfer: (data: { imei: string; transfer_type: string; notes?: string }) =>
    api.post("/device-check/transfer", data),
  transferOut: (data: { imei: string; new_owner_cnic: string; transfer_type: string; notes?: string }) =>
    api.post("/device-check/transfer-out", data),
};

export const adminApi = {
  listShopKeepers: (verified?: boolean) =>
    api.get("/admin/shop-keepers", { params: verified !== undefined ? { verified } : {} }),
  approveShop: (userId: number) => api.put(`/admin/shop-keepers/${userId}/approve`),
  suspendShop: (userId: number) => api.put(`/admin/shop-keepers/${userId}/suspend`),
  searchImei: (imei: string) => api.get<MobileDevice>(`/admin/search-imei/${imei}`),
  blockDevice: (deviceId: number) => api.put<MobileDevice>(`/admin/mobiles/${deviceId}/block`),
  unblockDevice: (deviceId: number) => api.put<MobileDevice>(`/admin/mobiles/${deviceId}/unblock`),
  getAuditLogs: (params?: { action_type?: string; limit?: number; offset?: number }) =>
    api.get<AuditLogEntry[]>("/admin/audit-logs", { params }),
  getAlerts: (params?: { is_reviewed?: boolean; limit?: number; offset?: number }) =>
    api.get<PoliceAlertRecord[]>("/admin/alerts", { params }),
  reviewAlert: (alertId: number) => api.put<PoliceAlertRecord>(`/admin/alerts/${alertId}/review`),
  getStats: () => api.get<AdminStats>("/admin/stats"),
  listSnatchReports: (params?: { is_reviewed?: boolean; limit?: number; offset?: number }) =>
    api.get<SnatchReport[]>("/admin/snatch-reports", { params }),
  reviewSnatchReport: (reportId: number) => api.put<SnatchReport>(`/admin/snatch-reports/${reportId}/review`),
};

export const transferOtpApi = {
  initiate: (data: { imei: string; old_owner_identifier: string }) =>
    api.post<InitiateTransferResponse>("/transfer-otp/initiate", data),
  verifyOldOwner: (data: { imei: string; old_owner_identifier: string; otp_code: string }) =>
    api.post<VerifyOldOwnerResponse>("/transfer-otp/verify-old-owner", data),
  sendNewOwnerOTP: (data: { imei: string; new_owner_identifier: string }) =>
    api.post<SendNewOwnerOTPResponse>("/transfer-otp/send-new-owner-otp", data),
  complete: (data: { imei: string; new_owner_identifier: string; otp_code: string; transfer_type: string; notes?: string }) =>
    api.post<CompleteTransferResponse>("/transfer-otp/complete", data),
};

export const snatchReportApi = {
  create: (data: { victim_cnic: string; device_imei: string; incident_description: string; incident_date?: string; incident_location?: string }) =>
    api.post<SnatchReport>("/snatch-reports", data),
  list: () => api.get<SnatchReport[]>("/snatch-reports"),
  getById: (id: number) => api.get<SnatchReport>(`/snatch-reports/${id}`),
};

export const reportsApi = {
  citizenDevices: () => api.get<MobileDevice[]>("/reports/citizen/my-devices"),
  citizenTransfers: () => api.get<TransferRecord[]>("/reports/citizen/my-transfers"),
  citizenStats: () => api.get<CitizenReportStats>("/reports/citizen/stats"),
  shopDevices: () => api.get<MobileDevice[]>("/reports/shop/registered-devices"),
  shopTransfers: () => api.get<TransferRecord[]>("/reports/shop/transfers-performed"),
  shopStats: () => api.get<ShopReportStats>("/reports/shop/stats"),
};

export default api;
