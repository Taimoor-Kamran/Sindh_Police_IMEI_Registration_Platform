"use client";

import { MobileDevice } from "@/lib/api";

interface DeviceTableProps {
  devices: MobileDevice[];
  showOwner?: boolean;
}

const statusColors: Record<string, string> = {
  active: "bg-green-100 text-green-700",
  stolen: "bg-red-100 text-red-700",
  blocked: "bg-gray-100 text-gray-700",
};

export default function DeviceTable({ devices, showOwner = false }: DeviceTableProps) {
  if (devices.length === 0) {
    return (
      <p className="text-center text-gray-400 py-8">No devices found</p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200">
            <th className="text-left py-3 px-4 font-medium text-gray-500">IMEI</th>
            <th className="text-left py-3 px-4 font-medium text-gray-500">Brand / Model</th>
            <th className="text-left py-3 px-4 font-medium text-gray-500">Mobile #</th>
            {showOwner && (
              <th className="text-left py-3 px-4 font-medium text-gray-500">Owner CNIC</th>
            )}
            <th className="text-left py-3 px-4 font-medium text-gray-500">Type</th>
            <th className="text-left py-3 px-4 font-medium text-gray-500">Status</th>
            <th className="text-left py-3 px-4 font-medium text-gray-500">Date</th>
          </tr>
        </thead>
        <tbody>
          {devices.map((device) => (
            <tr key={device.id} className="border-b border-gray-100 hover:bg-gray-50">
              <td className="py-3 px-4 font-mono text-xs">{device.imei}</td>
              <td className="py-3 px-4">
                {device.brand || "-"} {device.model ? `/ ${device.model}` : ""}
              </td>
              <td className="py-3 px-4">{device.mobile_number}</td>
              {showOwner && (
                <td className="py-3 px-4 font-mono text-xs">{device.current_owner_cnic}</td>
              )}
              <td className="py-3 px-4">
                <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                  device.registration_type === "SHOP" ? "bg-yellow-100 text-yellow-700" : "bg-blue-100 text-blue-700"
                }`}>
                  {device.registration_type}
                </span>
              </td>
              <td className="py-3 px-4">
                <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                  statusColors[device.status] || "bg-gray-100 text-gray-700"
                }`}>
                  {device.status}
                </span>
              </td>
              <td className="py-3 px-4 text-gray-500">
                {new Date(device.registration_date).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
