import {
  Activity,
  FileCheck,
  Bot,
  FileText,
  LayoutDashboard,
  Network,
  Radar,
  ScanSearch,
  Settings,
  ShieldCheck,
  X,
} from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navigation = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    label: "Network Analyzer",
    icon: Network,
    path: "/network",
  },
  {
    label: "Vulnerability Scanner",
    icon: ScanSearch,
    path: "/vulnerabilities",
  },
  {
    label: "File Integrity",
    icon: FileCheck,
    path: "/file-integrity",
  },
  {
    label: "Web Security",
    icon: ShieldCheck,
    path: "/web-security",
  },
  {
    label: "Threat Intelligence",
    icon: Radar,
    path: "/threat-intel",
  },
  {
    label: "AI Assistant",
    icon: Bot,
    path: "/ai-assistant",
  },
  {
    label: "Reports",
    icon: FileText,
    path: "/reports",
  },
  {
    label: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-white/10 bg-[#111827] transition-transform duration-300 lg:static lg:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex h-16 items-center justify-between border-b border-white/10 px-5">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#00F0FF]/10">
              <ShieldCheck className="h-5 w-5 text-[#00F0FF]" />
            </div>

            <div>
              <h1 className="text-sm font-bold text-white">
                CyberShield <span className="text-[#00F0FF]">AI</span>
              </h1>

              <p className="text-[10px] text-gray-500">
                DEFENSIVE SECURITY
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="rounded-md p-1 text-gray-400 hover:bg-white/5 hover:text-white lg:hidden"
            aria-label="Close navigation"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          <p className="mb-3 px-3 pt-2 text-[10px] font-semibold uppercase tracking-wider text-gray-500">
            Security Operations
          </p>

          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <a
                key={item.path}
                href={item.path}
                onClick={onClose}
                className="group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-gray-400 transition hover:bg-[#00F0FF]/10 hover:text-[#00F0FF]"
              >
                <Icon className="h-4 w-4" />

                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>

        <div className="border-t border-white/10 p-4">
          <div className="flex items-center gap-3 rounded-lg bg-[#0B0F17] p-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#00F0FF]/10">
              <Activity className="h-4 w-4 text-[#10B981]" />
            </div>

            <div>
              <p className="text-xs font-medium text-white">
                System Status
              </p>

              <p className="text-[10px] text-[#10B981]">
                All systems operational
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

