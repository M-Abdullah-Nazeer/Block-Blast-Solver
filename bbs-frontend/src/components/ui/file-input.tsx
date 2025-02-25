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
import { Icons } from '../icons'
import Image from 'next/image'

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {

  uploadedFile: File | null
  setUploadedFile: (file: File | null) => void

}

const FileInput = forwardRef<HTMLInputElement, InputProps>(
  ({ className, uploadedFile, setUploadedFile, ...props }, ref) => {
    const { toast } = useToast()
    const [dragActive, setDragActive] = useState<boolean>(false)
    const [uploading, setUploading] = useState<boolean>(false)

    // handle drag events
    const handleDrag = (e: DragEvent<HTMLFormElement | HTMLDivElement>) => {
      e.preventDefault()
      e.stopPropagation()
      if (e.type === 'dragenter' || e.type === 'dragover') {
        setDragActive(true)
      } else if (e.type === 'dragleave') {
        setDragActive(false)
      }
    }

    // Handle file selection
    const handleChange = async (e: ChangeEvent<HTMLInputElement>) => {
      e.preventDefault()
      if (e.target.files && e.target.files[0]) {
        const file = e.target.files[0]

        // Validate file type
        if (!validateFileType(file)) {
          toast({
            title: 'Invalid file type',
            description: 'Please upload a valid image file.',
          })
          return
        }

        // Only allow one file
        setUploadedFile(file)
        await uploadFile(file)
      }
    }

    // Handle file drop
    const handleDrop = async (e: DragEvent<HTMLDivElement>) => {
      e.preventDefault()
      e.stopPropagation()

      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        const file = e.dataTransfer.files[0]

        // Validate file type
        if (!validateFileType(file)) {
          toast({
            title: 'Invalid file type',
            description: 'Please upload a valid image file.',
          })
          return
        }

        // Only allow one file
        setUploadedFile(file)
        await uploadFile(file)
      }
    }

    // Function to upload image to backend
    const uploadFile = async (file: File) => {
      setUploading(true)

      try {
        const formData = new FormData()
        formData.append('image', file)

        const response = await axios.post('/api/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        toast({
          title: 'Upload successful',
          description: 'Your image has been uploaded.',
        })
      } catch (error) {
        toast({
          title: 'Upload failed',
          description: 'There was an error uploading the image.',
        })
      } finally {
        setUploading(false)
      }
    }

    return (
      <form
        onSubmit={(e) => e.preventDefault()}
        onDragEnter={handleDrag}
        className="flex items-center w-full lg:w-1/2 justify-start bg-[#0f172d] rounded-lg"
      >
        <label
          htmlFor="dropzone-file"
          className={cn(
            'group relative h-full flex flex-col items-center justify-center w-full aspect-square lg:aspect-video md:aspect-video border-4 border-[#9ac8f6] border-dashed rounded-lg dark:border-[#9ac8f6] transition',
            { 'dark:hover:border-[#fff] dark:hover:bg-[#254083]': dragActive }
          )}
        >
          <div
            className="relative w-full h-full flex flex-col items-center justify-center"
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
                  <p className="text-xs text-gray-400">{(uploadedFile.size / 1000000).toFixed(2)} MB</p>
                </div>
              </div>
            ) : (
              <>
                <div
                  className="absolute inset-0 cursor-pointer"
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                />

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

                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag
                  and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Only 1 image, max 5MB
                </p>

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
        </label>
      </form>
    )
  }
)

FileInput.displayName = 'FileInput'

export { FileInput }
