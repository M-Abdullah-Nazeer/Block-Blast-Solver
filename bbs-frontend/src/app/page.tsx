'use client'

import { FC, useState } from 'react'
import { Button, buttonVariants } from '@/ui/button'
import { FileInput } from '@/ui/file-input'
import example from "public/example.png"
import manualIcon from "public/manual-icon.png"
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import Image from 'next/image'

export const metadata = {
  title: 'ImageToAlt - Home',
}

const Page: FC = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  // Function to clear the uploaded file
  const clearFile = () => {
    setUploadedFile(null)
  }

  return (
    <section className="container grid items-center gap-6 pt-6 pb-8 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        {/* <h1 className="text-3xl font-extrabold leading-tight tracking-tighter sm:text-3xl md:text-5xl lg:text-6xl">
          Block Blast Solver Online
        </h1>
        <p className="max-w-[700px] text-lg text-slate-700 dark:text-slate-400 sm:text-xl">
          Get Block Blast high score solution by taking screenshots
        </p> */}
      </div>

      {/* Upload Section */}
      <div className="flex flex-col lg:flex-row md:flex-row gap-4 lg:gap-20 justify-center items-stretch bg-[#274aa6] py-8 px-2 lg:p-10 rounded-lg">
        {/* Pass uploadedFile state and setter to FileInput */}
        <FileInput uploadedFile={uploadedFile} setUploadedFile={setUploadedFile} />

        <div className="flex flex-col justify-center items-center gap-4 w-full lg:w-1/2 md:w-1/2 bg-[#0f172d] rounded-lg py-8 px-2 lg:p-10">

          <Image
            className="rounded-lg"
            src={example}
            alt="Uploaded Preview"
            width={150}
            height={150}
            loading="lazy"
          />


          <span>OR</span>

          <button className="flex items-center justify-center gap-3 bg-[#468beb] text-white p-[16px] lg:px-[24px] lg:py-[16px] rounded-lg hover:bg-[#316edf] w-[200px] lg:w-[252px] h-[56px]">
            <Image alt="select image" className="w-[32px] h-[32px] aspect-square" src={manualIcon} />
            <span className="text-18px font-semibold leading-24px text-center">Fill Manually</span>
          </button>
        </div>
      </div>

      {/* Try Another Button */}

      {uploadedFile && (



        <Tooltip>
          <TooltipTrigger asChild>
            <div className="w-fit mx-auto lg:mx-0 lg:my-4 md:mx-auto md:my-4">
              <Button
                disabled={!uploadedFile}
                className={buttonVariants({ size: 'lg', className: 'w-fit' })}
                onClick={clearFile}
              >
                Try Another
              </Button>
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <p>Get results for next move</p>
          </TooltipContent>
        </Tooltip>
      )}

      {/* Legal disclaimers */}
      <div className="flex flex-col gap-4 mt-12">
        {/* <p className="text-slate-400 text-sm">
          All images are used solely for alt-generation and are automatically deleted after 24h.
        </p> */}
        <div className="flex items-center gap-4">
          <Button href="/terms" className={buttonVariants({ variant: 'link', size: 'sm' })}>
            Terms
          </Button>
          <Button href="/privacy-policy" className={buttonVariants({ variant: 'link', size: 'sm' })}>
            Privacy Policy
          </Button>
        </div>
      </div>
    </section>
  )
}

export default Page
