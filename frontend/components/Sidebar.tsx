"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Smartphone,
  Users,
  FileText,
  User,
  Shield,
  ShieldAlert,
  X,
  Plus,
  Store,
  Search,
  ScrollText,
  LayoutDashboard,
  ArrowRightLeft,
  BarChart3,
} from "lucide-react";
import { getUserRole } from "@/lib/auth";

interface NavItem {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

const citizenNav: NavItem[] = [
  { href: "/dashboard", label: "My Mobiles", icon: Smartphone },
  { href: "/dashboard/register-device", label: "Register Device", icon: Plus },
  { href: "/dashboard/transfer", label: "Transfer Ownership", icon: ArrowRightLeft },
  { href: "/dashboard/report", label: "Report Snatching", icon: FileText },
  { href: "/dashboard/reports", label: "My Reports", icon: BarChart3 },
  { href: "/dashboard/profile", label: "My Profile", icon: User },
];

const shopKeeperNav: NavItem[] = [
  { href: "/dashboard", label: "My Registrations", icon: Smartphone },
  { href: "/dashboard/register-device-shop", label: "Register for Customer", icon: Store },
  { href: "/dashboard/transfer", label: "Transfer Ownership", icon: ArrowRightLeft },
  { href: "/dashboard/report", label: "Report Snatching", icon: FileText },
  { href: "/dashboard/reports", label: "Shop Reports", icon: BarChart3 },
  { href: "/dashboard/profile", label: "My Profile", icon: User },
];

const adminNav: NavItem[] = [
  { href: "/dashboard/admin", label: "Admin Overview", icon: LayoutDashboard },
  { href: "/dashboard/admin/alerts", label: "Police Alerts", icon: ShieldAlert },
  { href: "/dashboard/admin/snatch-reports", label: "Snatching Reports", icon: FileText },
  { href: "/dashboard/admin/shops", label: "Manage Shops", icon: Store },
  { href: "/dashboard/admin/search", label: "IMEI Search", icon: Search },
  { href: "/dashboard/admin/audit", label: "Audit Logs", icon: ScrollText },
  { href: "/dashboard/profile", label: "My Profile", icon: User },
];

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const role = getUserRole();

  const navItems =
    role === "police_admin"
      ? adminNav
      : role === "shop_keeper"
      ? shopKeeperNav
      : citizenNav;

  const isActive = (href: string) => {
    if (href === "/dashboard") {
      return pathname === "/dashboard";
    }
    return pathname === href || pathname.startsWith(href + "/");
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 left-0 z-50 h-full w-64 bg-primary text-white flex flex-col transition-transform duration-300 lg:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Logo Section */}
        <div className="flex items-center justify-between p-5 border-b border-primary-light">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent rounded-full flex items-center justify-center">
              <Shield className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h2 className="font-bold text-sm leading-tight">Sindh Police</h2>
              <p className="text-xs text-gray-300">IMEI Platform</p>
            </div>
          </div>
          <button onClick={onClose} className="lg:hidden text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                  active
                    ? "bg-accent text-primary"
                    : "text-gray-200 hover:bg-primary-light hover:text-white"
                }`}
              >
                <Icon className="w-5 h-5" />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-primary-light">
          <p className="text-xs text-gray-400 text-center">
            &copy; 2024 Sindh Police
          </p>
        </div>
      </aside>
    </>
  );
}
