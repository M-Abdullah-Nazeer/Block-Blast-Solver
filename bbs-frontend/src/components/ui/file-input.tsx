'use client'
import {
  forwardRef,
  useState,
  type ChangeEvent,
  type DragEvent,
} from 'react'
import axios from 'axios'
import { useToast } from '@/src/hooks/use-toast'
import { cn, validateFileType } from '@/lib/utils'
import { useTab } from '../../context/TabContext';
import Image from 'next/image'

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  uploadedFile: File | null
  setUploadedFile: (file: File | null) => void
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>
  onUploadSuccess: (steps: { board: number[][]; completedLines: number }[], shapeColors: Record<string, string>) => void;
}

const FileInput = forwardRef<HTMLInputElement, InputProps>(
  ({ className, uploadedFile, setUploadedFile, setIsLoading, onUploadSuccess, ...props }, ref) => {
    const { toast } = useToast()
    const [dragActive, setDragActive] = useState<boolean>(false)
    const [uploading, setUploading] = useState<boolean>(false)
    const { setActiveTab } = useTab();

    const API_URL = "/api/";
    const API_KEY = "d5Kf9ul2jH7sRmADPqlahVYBzXeABDM13LKg2aTd4GFu21FJ8NcOWqElU59x785AYFEBt";

    const handleDrag = (e: DragEvent<HTMLFormElement | HTMLDivElement | HTMLLabelElement>) => {
      e.preventDefault()
      e.stopPropagation()
      if (e.type === 'dragenter' || e.type === 'dragover') {
        setDragActive(true)
      } else if (e.type === 'dragleave') {
        setDragActive(false)
      }
    }
    const handleChange = async (e: ChangeEvent<HTMLInputElement>) => {
      e.preventDefault()
      if (e.target.files && e.target.files[0]) {
        const file = e.target.files[0]
        if (!validateFileType(file)) {
          toast({
            title: 'Invalid file type',
            description: 'Please upload a valid image file (JPG/JPEG/PNG).',
          })
          return
        }
        setUploadedFile(file)
        await uploadFile(file)
      }
    }
    const handleDrop = async (e: DragEvent<HTMLDivElement | HTMLLabelElement>) => {
      e.preventDefault()
      e.stopPropagation()
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        const file = e.dataTransfer.files[0]
        if (!validateFileType(file)) {
          toast({
            title: 'Invalid file type',
            description: 'Please upload a valid image file.',
          })
          return
        }
        setUploadedFile(file)
        await uploadFile(file)
      }
    }
    const uploadFile = async (file: File) => {
      setUploading(true)
      try {
        setIsLoading(true);
        const formData = new FormData()
        formData.append('file', file)
        if (!API_KEY) {
          throw new Error("API key is missing!");
          return;
        }
        const response = await axios.post(`${API_URL}upload`, formData, {
          headers: {
            'X-API-Key': API_KEY
          },
        })
        toast({
          title: 'Upload successful',
          description: 'Your image has been uploaded.',
        })
        if (response.data.final_output && response.data.shape_colors) {
          const processedSteps = response.data.final_output.map((step: any) => ({
            board: step.board,
            completedLines: step.completedLines,
          }));
          setActiveTab(3);
          onUploadSuccess(processedSteps, response.data.shape_colors);
        }

      } catch (error) {   
        toast({
          title: 'Upload failed',
          description: 'There was an error uploading the image.',
        })
      } finally {
        setUploading(false)
        setIsLoading(false);

      }

    }

    return (
<form
  onSubmit={(e) => e.preventDefault()}
  onDragEnter={handleDrag}
  className="flex items-center w-full lg:w-1/2 justify-start bg-[#0f172d] rounded-lg z-10"
>
  <div
    className={cn(
      'group relative h-full flex flex-col items-center justify-center w-full aspect-square lg:aspect-video md:aspect-video border-4 border-[#9ac8f6] border-solid rounded-lg dark:border-[#9ac8f6] transition',
      { 'dark:hover:border-[#fff] dark:hover:bg-[#254083]': dragActive }
    )}
  >
    {uploadedFile ? (
      <div>
        <Image
          src={URL.createObjectURL(uploadedFile)}
          alt="Uploaded Preview"
          width={70}
          height={70}
          className="object-cover rounded-lg mx-auto mb-2 lg:w-[100px] lg:h-[auto] md:w-[100px] md:h-[auto]"
        />
        <div className="text-center">
          <p className="text-sm text-gray-500">{uploadedFile.name}</p>
          <p className="text-xs text-gray-400">
            {(uploadedFile.size / 1000000).toFixed(2)} MB
          </p>
        </div>
      </div>
    ) : (
      <>
        <label
          htmlFor="dropzone-file"
          className="relative w-full h-full flex flex-col items-center justify-center cursor-pointer"
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <svg
            aria-hidden="true"
            className="w-10 h-10 mb-3 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            ></path>
          </svg>

          <span className="mb-2 text-sm text-gray-500 dark:text-gray-400">
            <span className="font-semibold">Click to upload</span> or drag and drop
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400">
            Only 1 image, max 20MB
          </span>
        </label>

        <input
          {...props}
          ref={ref}
          onChange={handleChange}
          accept="image/jpeg, image/jpg, image/png"
          id="dropzone-file"
          type="file"
          className="hidden"
        />
      </>
    )}
  </div>
</form>
    )
  }
)
FileInput.displayName = 'FileInput'
export { FileInput }