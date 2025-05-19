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

// export interface InputProps
//   extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {

//   uploadedFile: File | null
//   setUploadedFile: (file: File | null) => void
//   onUploadSuccess: (steps: number[][][], shapeColors: Record<string, string>) => void;
// }


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


    // const API_URL = "http://localhost:8000";
    const API_URL = "http://backend:8000";
    // const API_URL = process.env.NEXT_PUBLIC_API_URL;
    const API_KEY = process.env.NEXT_PUBLIC_API_KEY;




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
            description: 'Please upload a valid image file (JPG/JPEG/PNG).',
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

        setIsLoading(true);

        const formData = new FormData()
        formData.append('file', file)

        if (!API_KEY) {
          // console.error("API key is missing!");
          throw new Error("API key is missing!");
          return;
        }

        const response = await axios.post(`${API_URL}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'X-API-Key': API_KEY

          },
        })
        // console.log('Response2:', response.data.final_output);
        toast({
          title: 'Upload successful',
          description: 'Your image has been uploaded.',
        })

        if (response.data.final_output && response.data.shape_colors) {
          // Ensure that final_output is an array of objects with `board` and `completedLines`
          const processedSteps = response.data.final_output.map((step: any) => ({
            board: step.board,
            completedLines: step.completedLines,
          }));

          setActiveTab(3);
          // Pass the processed data to the parent component
          onUploadSuccess(processedSteps, response.data.shape_colors);
        }

      } catch (error) {
        // alert(`Backend URL: ${API_URL}`);
        // alert("Backend URL:" + error);
        // console.log(error);
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
        <label
          htmlFor="dropzone-file"
          className={cn(
            'group relative h-full flex flex-col items-center justify-center w-full aspect-square lg:aspect-video md:aspect-video border-4 border-[#9ac8f6] border-solid rounded-lg dark:border-[#9ac8f6] transition',
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








// 'use client'

// import {
//   forwardRef,
//   useState,
//   useEffect,
//   type ChangeEvent,
//   type DragEvent,
// } from 'react'
// import axios from 'axios'
// import { useToast } from '@/src/hooks/use-toast'
// import { cn, validateFileType } from '@/lib/utils'
// import { Icons } from '../icons'
// import Image from 'next/image'

// export interface InputProps
//   extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {

//   uploadedFile: File | null
//   setUploadedFile: (file: File | null) => void

// }

// const FileInput = forwardRef<HTMLInputElement, InputProps>(
//   ({ className, uploadedFile, setUploadedFile, ...props }, ref) => {
//     const { toast } = useToast()
//     const [dragActive, setDragActive] = useState<boolean>(false)
//     const [uploading, setUploading] = useState<boolean>(false)
//     const [previewUrl, setPreviewUrl] = useState<string | null>(null)

//     let cancelTokenSource = axios.CancelToken.source()

//     // Handle cleanup of blob URLs
//     useEffect(() => {
//       if (uploadedFile) {
//         const objectUrl = URL.createObjectURL(uploadedFile)
//         setPreviewUrl(objectUrl)

//         return () => {
//           URL.revokeObjectURL(objectUrl)
//         }
//       }
//     }, [uploadedFile])

//     // Handle drag events
//     const handleDrag = (e: DragEvent<HTMLFormElement | HTMLDivElement>) => {
//       e.preventDefault()
//       e.stopPropagation()
//       setDragActive(e.type === 'dragenter' || e.type === 'dragover')
//     }

//     // Handle file selection
//     const handleChange = async (e: ChangeEvent<HTMLInputElement>) => {
//       e.preventDefault()
//       if (e.target.files && e.target.files[0]) {
//         const file = e.target.files[0]

//         // Validate file type
//         if (!validateFileType(file)) {
//           toast({ title: 'Invalid file type', description: 'Please upload a valid image file.' })
//           return
//         }

//         // Store a persistent reference
//         const newFile = new File([file], file.name, { type: file.type })
//         setUploadedFile(newFile)
//         await uploadFile(newFile)

//         // Reset file input
//         e.target.value = ''
//       }
//     }

//     // Handle file drop
//     const handleDrop = async (e: DragEvent<HTMLDivElement>) => {
//       e.preventDefault()
//       e.stopPropagation()

//       if (e.dataTransfer.files && e.dataTransfer.files[0]) {
//         const file = e.dataTransfer.files[0]

//         // Validate file type
//         if (!validateFileType(file)) {
//           toast({ title: 'Invalid file type', description: 'Please upload a valid image file.' })
//           return
//         }

//         setUploadedFile(file)
//         await uploadFile(file)
//       }
//     }

//     // Function to upload image to backend
//     const uploadFile = async (file: File) => {
//       if (cancelTokenSource) {
//         cancelTokenSource.cancel("Previous upload canceled.")
//       }
//       cancelTokenSource = axios.CancelToken.source()

//       setUploading(true)
//       try {
//         const formData = new FormData()
//         formData.append('file', file)

//         const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' },
//           cancelToken: cancelTokenSource.token,
//         })
//         console.log('Response:', response.data)
//         toast({ title: 'Upload successful', description: 'Your image has been uploaded.' })
//       } catch (error) {
//         if (axios.isCancel(error)) {
//           console.log('Upload canceled:', error.message)
//         } else {
//           toast({ title: 'Upload failed', description: 'There was an error uploading the image.' })
//         }
//       } finally {
//         setUploading(false)
//       }
//     }

//     return (
//       <form
//         onSubmit={(e) => e.preventDefault()}
//         onDragEnter={handleDrag}
//         className="flex items-center w-full lg:w-1/2 justify-start bg-[#0f172d] rounded-lg"
//       >
//         <label
//           htmlFor="dropzone-file"
//           className={cn(
//             'group relative h-full flex flex-col items-center justify-center w-full aspect-square lg:aspect-video md:aspect-video border-4 border-[#9ac8f6] border-dashed rounded-lg dark:border-[#9ac8f6] transition',
//             { 'dark:hover:border-[#fff] dark:hover:bg-[#254083]': dragActive }
//           )}
//         >
//           <div className="relative w-full h-full flex flex-col items-center justify-center">
//             {uploadedFile ? (
//               <div>
//                 {previewUrl && (
//                   <Image
//                     src={previewUrl}
//                     alt="Uploaded Preview"
//                     width={70}
//                     height={70}
//                     className="object-cover rounded-lg mx-auto mb-2 lg:w-[100px] lg:h-[auto] md:w-[100px] md:h-[auto]"
//                   />
//                 )}

//                 <div className="text-center">
//                   <p className="text-sm text-gray-500">{uploadedFile.name}</p>
//                   <p className="text-xs text-gray-400">{(uploadedFile.size / 1000000).toFixed(2)} MB</p>
//                 </div>
//               </div>
//             ) : (
//               <>
//                 <div
//                   className="absolute inset-0 cursor-pointer"
//                   onDragEnter={handleDrag}
//                   onDragLeave={handleDrag}
//                   onDragOver={handleDrag}
//                   onDrop={handleDrop}
//                 />

//                 <svg
//                   aria-hidden="true"
//                   className="w-10 h-10 mb-3 text-gray-400"
//                   fill="none"
//                   stroke="currentColor"
//                   viewBox="0 0 24 24"
//                   xmlns="http://www.w3.org/2000/svg"
//                 >
//                   <path
//                     strokeLinecap="round"
//                     strokeLinejoin="round"
//                     strokeWidth="2"
//                     d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
//                   ></path>
//                 </svg>

//                 <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
//                   <span className="font-semibold">Click to upload</span> or drag and drop
//                 </p>
//                 <p className="text-xs text-gray-500 dark:text-gray-400">
//                   Only 1 image, max 5MB
//                 </p>

//                 <input
//                   {...props}
//                   ref={ref}
//                   onChange={handleChange}
//                   accept="image/jpeg, image/jpg, image/png"
//                   id="dropzone-file"
//                   type="file"
//                   className="hidden"
//                 />
//               </>
//             )}
//           </div>
//         </label>
//       </form>
//     )
//   }
// )

// FileInput.displayName = 'FileInput'

// export { FileInput }
