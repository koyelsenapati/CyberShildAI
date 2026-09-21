interface PageHeaderProps {
  eyebrow?: string;
  title: string;
  description: string;
  action?: React.ReactNode;
}

export default function PageHeader({
  eyebrow = "SECURITY OPERATIONS",
  title,
  description,
  action,
}: PageHeaderProps) {
  return (
    <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
      <div>
        <p className="text-xs font-medium uppercase tracking-wider text-[#00F0FF]">
          {eyebrow}
        </p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-white md:text-3xl">
          {title}
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-gray-500">
          {description}
        </p>
      </div>

      {action && <div>{action}</div>}
    </div>
  );
}
