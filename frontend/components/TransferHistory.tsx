"use client";

import { TransferRecord } from "@/lib/api";
import { ArrowRight } from "lucide-react";

interface TransferHistoryProps {
  transfers: TransferRecord[];
}

export default function TransferHistory({ transfers }: TransferHistoryProps) {
  if (transfers.length === 0) {
    return (
      <p className="text-center text-gray-400 py-8">No transfer history</p>
    );
  }

  return (
    <div className="space-y-3">
      {transfers.map((transfer) => (
        <div
          key={transfer.id}
          className="bg-gray-50 rounded-lg p-4 border border-gray-100"
        >
          <div className="flex items-center gap-2 text-sm">
            <span className="font-mono text-xs text-gray-600">
              {transfer.old_owner_cnic}
            </span>
            <ArrowRight className="w-4 h-4 text-gray-400" />
            <span className="font-mono text-xs text-gray-600">
              {transfer.new_owner_cnic}
            </span>
          </div>
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
            <span className="bg-primary/10 text-primary px-2 py-0.5 rounded font-medium">
              {transfer.transfer_type}
            </span>
            <span>IMEI: {transfer.imei}</span>
            <span>
              {new Date(transfer.transfer_date).toLocaleDateString()}
            </span>
          </div>
          {transfer.notes && (
            <p className="text-xs text-gray-400 mt-2">{transfer.notes}</p>
          )}
        </div>
      ))}
    </div>
  );
}
