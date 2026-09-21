import {
  Download,
  FileText,
  Plus,
} from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";
import EmptyState from "../components/common/EmptyState";

export default function Reports() {
  return (
    <DashboardLayout>
      <div className="mx-auto max-w-[1600px] space-y-6">
        <PageHeader
          eyebrow="SECURITY REPORTING"
          title="Reports"
          description="View, download, and manage generated cybersecurity assessment reports."
          action={
            <button className="flex items-center gap-2 rounded-lg bg-[#00F0FF] px-4 py-2.5 text-xs font-semibold text-[#0B0F17]">
              <Plus className="h-4 w-4" />
              Generate Report
            </button>
          }
        />

        <EmptyState
          icon={FileText}
          title="No Reports Available"
          description="Generated security reports will appear here. Reports can later be exported as PDF or HTML."
        />

        <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-[#1F2937]/50 p-4">
          <Download className="h-5 w-5 text-[#00F0FF]" />

          <p className="text-xs text-gray-500">
            PDF report generation will connect to the backend reporting service.
          </p>
        </div>
      </div>
    </DashboardLayout>
  );
}
