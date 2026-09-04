import { FC, ChangeEvent, DragEvent, useState } from 'react';
import { UploadCloud, X, Image as ImageIcon } from 'lucide-react';

export interface ImageUploaderProps {
  files?: File[];
  onChange?: (files: File[]) => void;
  maxFiles?: number;
  maxSizeMB?: number;
  label?: string;
  error?: string;
}

export const ImageUploader: FC<ImageUploaderProps> = ({
  files = [],
  onChange,
  maxFiles = 4,
  maxSizeMB = 5,
  label = 'Upload Image Evidence',
  error,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [internalError, setInternalError] = useState<string | null>(null);

  const validateAndAdd = (newFiles: File[]) => {
    setInternalError(null);
    const valid: File[] = [];

    for (const file of newFiles) {
      if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
        setInternalError('Only JPG, PNG, and WebP images are allowed.');
        return;
      }
      if (file.size > maxSizeMB * 1024 * 1024) {
        setInternalError(`File size must not exceed ${maxSizeMB}MB.`);
        return;
      }
      valid.push(file);
    }

    if (files.length + valid.length > maxFiles) {
      setInternalError(`Maximum ${maxFiles} images allowed.`);
      return;
    }

    onChange?.([...files, ...valid]);
  };

  const handleFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      validateAndAdd(Array.from(e.target.files));
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files) {
      validateAndAdd(Array.from(e.dataTransfer.files));
    }
  };

  const removeFile = (index: number) => {
    const updated = files.filter((_, i) => i !== index);
    onChange?.(updated);
  };

  return (
    <div className="flex w-full flex-col gap-2">
      {label && <label className="text-sm font-medium text-slate-700">{label}</label>}

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-6 text-center transition cursor-pointer ${
          isDragging
            ? 'border-[#2563EB] bg-[#EFF6FF]'
            : 'border-slate-300 bg-slate-50 hover:bg-slate-100/80'
        }`}
      >
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          id="image-uploader-input"
          disabled={files.length >= maxFiles}
        />
        <label htmlFor="image-uploader-input" className="cursor-pointer flex flex-col items-center">
          <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-white text-[#2563EB] shadow-xs border border-slate-200">
            <UploadCloud className="h-6 w-6" />
          </div>
          <p className="text-sm font-semibold text-slate-700">
            Click to upload <span className="font-normal text-slate-500">or drag & drop</span>
          </p>
          <p className="text-xs text-slate-400 mt-1">
            JPG, PNG or WebP (max {maxSizeMB}MB per image, up to {maxFiles} images)
          </p>
        </label>
      </div>

      {(error || internalError) && (
        <p className="text-xs font-medium text-rose-600 animate-fade-in">
          {error || internalError}
        </p>
      )}

      {files.length > 0 && (
        <div className="mt-2 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {files.map((file, idx) => {
            const url = URL.createObjectURL(file);
            return (
              <div key={idx} className="relative group rounded-xl border border-slate-200 overflow-hidden bg-white shadow-xs">
                <img src={url} alt={file.name} className="h-24 w-full object-cover" />
                <button
                  type="button"
                  onClick={() => removeFile(idx)}
                  className="absolute top-1 right-1 rounded-full bg-slate-900/70 p-1 text-white hover:bg-rose-600 transition"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
                <div className="p-1.5 flex items-center gap-1 text-[11px] text-slate-600 truncate">
                  <ImageIcon className="h-3 w-3 shrink-0" />
                  <span className="truncate">{file.name}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
