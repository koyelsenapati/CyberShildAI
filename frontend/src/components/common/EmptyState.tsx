import type { LucideIcon } from "lucide-react";

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export default function EmptyState({
  icon: Icon,
  title,
  description,
}: EmptyStateProps) {
  return (
    <div className="flex min-h-[350px] items-center justify-center rounded-xl border border-white/10 bg-[#1F2937]/50">
      <div className="max-w-md px-6 text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-xl border border-[#00F0FF]/10 bg-[#00F0FF]/5">
          <Icon className="h-7 w-7 text-[#00F0FF]" />
        </div>

        <h2 className="mt-4 text-base font-semibold text-white">
          {title}
        </h2>

        <p className="mt-2 text-sm leading-6 text-gray-500">
          {description}
        </p>
      </div>
    </div>
  );
}
