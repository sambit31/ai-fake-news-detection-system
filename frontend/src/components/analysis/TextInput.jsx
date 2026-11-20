export default function TextInput({
  title,
  setTitle,
  articleText,
  setArticleText,
}) {
  return (
    <div className="space-y-5">
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Article headline (optional)
        </label>

        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter the news headline..."
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
        />
      </div>

      <div>
        <div className="mb-2 flex justify-between">
          <label className="text-sm font-medium text-slate-300">
            News article
          </label>

          <span className="text-xs text-slate-500">
            {articleText.length} characters
          </span>
        </div>

        <textarea
          rows={10}
          value={articleText}
          onChange={(e) => setArticleText(e.target.value)}
          placeholder="Paste the complete news article here..."
          className="w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-4 text-sm leading-7 outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
        />
      </div>
    </div>
  );
}
