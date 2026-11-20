import { Upload, X } from "lucide-react";

export default function PDFInput({ file, setFile, resetResult }) {
  return (
    <div>
      <label
        htmlFor="pdf-upload"
        className="flex min-h-64 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-700 bg-slate-950 p-8 text-center transition hover:border-blue-500 hover:bg-blue-500/5"
      >
        <div className="mb-4 rounded-2xl bg-blue-500/10 p-4 text-blue-400">
          <Upload size={32} />
        </div>

        <p className="font-semibold">
          {file ? file.name : "Upload your news PDF"}
        </p>

        <p className="mt-2 text-sm text-slate-400">
          {file
            ? "PDF selected successfully"
            : "Click to browse and select a PDF file"}
        </p>

        <p className="mt-3 text-xs text-slate-500">
          Maximum file size: 10 MB
        </p>

        <input
          id="pdf-upload"
          type="file"
          accept=".pdf,application/pdf"
          className="hidden"
          onChange={(e) => {
            const selectedFile = e.target.files?.[0];

            if (selectedFile) {
              setFile(selectedFile);
              resetResult();
            }
          }}
        />
      </label>

      {file && (
        <button
          type="button"
          onClick={() => setFile(null)}
          className="mt-3 flex items-center gap-2 text-sm text-red-400 hover:text-red-300"
        >
          <X size={16} />
          Remove selected file
        </button>
      )}
    </div>
  );
}
