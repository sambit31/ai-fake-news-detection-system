import { Link as LinkIcon } from "lucide-react";

export default function URLInput({ url, setUrl }) {
  return (
    <div className="py-8">
      <label className="mb-3 block text-sm font-medium text-slate-300">
        News article URL
      </label>

      <div className="flex items-center gap-3 rounded-xl border border-slate-700 bg-slate-950 px-4 py-1 focus-within:border-blue-500">
        <LinkIcon size={19} className="shrink-0 text-slate-500" />

        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/news/article"
          className="w-full bg-transparent py-4 text-sm outline-none placeholder:text-slate-600"
        />
      </div>

      <p className="mt-3 text-xs text-slate-500">
        Use a publicly accessible individual news article URL.
      </p>
    </div>
  );
}
