interface RoleBadgeProps {
  role: string;
}

const roleConfig: Record<string, { label: string; className: string }> = {
  citizen: {
    label: "Citizen",
    className: "bg-blue-100 text-blue-700",
  },
  shop_keeper: {
    label: "Shop Keeper",
    className: "bg-yellow-100 text-yellow-700",
  },
  police_admin: {
    label: "Police Admin",
    className: "bg-primary/10 text-primary",
  },
};

export default function RoleBadge({ role }: RoleBadgeProps) {
  const config = roleConfig[role] || {
    label: role,
    className: "bg-gray-100 text-gray-700",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.className}`}
    >
      {config.label}
    </span>
  );
}
