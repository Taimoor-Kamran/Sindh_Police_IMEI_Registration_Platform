import { type LucideIcon } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: number;
  icon: LucideIcon;
  color: "green" | "gold" | "blue" | "red";
}

const colorMap = {
  green: "bg-primary/10 text-primary",
  gold: "bg-accent/20 text-yellow-700",
  blue: "bg-blue-50 text-blue-600",
  red: "bg-red-50 text-red-600",
};

const iconBgMap = {
  green: "bg-primary",
  gold: "bg-accent",
  blue: "bg-blue-500",
  red: "bg-red-500",
};

export default function StatsCard({ title, value, icon: Icon, color }: StatsCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 font-medium">{title}</p>
          <p className="text-3xl font-bold text-gray-800 mt-1">{value}</p>
        </div>
        <div
          className={`w-12 h-12 rounded-xl flex items-center justify-center ${iconBgMap[color]}`}
        >
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );
}
