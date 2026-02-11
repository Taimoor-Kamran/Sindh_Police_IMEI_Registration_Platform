import { UserInfo } from "./api";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export function setToken(token: string): void {
  localStorage.setItem("token", token);
}

export function removeToken(): void {
  localStorage.removeItem("token");
}

export function getUser(): UserInfo | null {
  if (typeof window === "undefined") return null;
  const user = localStorage.getItem("user");
  if (!user) return null;
  try {
    return JSON.parse(user);
  } catch {
    return null;
  }
}

export function setUser(user: UserInfo): void {
  localStorage.setItem("user", JSON.stringify(user));
}

export function removeUser(): void {
  localStorage.removeItem("user");
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export function logout(): void {
  removeToken();
  removeUser();
}

export function getUserRole(): string {
  const user = getUser();
  return user?.role || "citizen";
}

export function isAdmin(): boolean {
  return getUserRole() === "police_admin";
}

export function isShopKeeper(): boolean {
  return getUserRole() === "shop_keeper";
}

export function isShopVerified(): boolean {
  const user = getUser();
  return user?.role === "shop_keeper" && user?.is_shop_verified === true;
}
