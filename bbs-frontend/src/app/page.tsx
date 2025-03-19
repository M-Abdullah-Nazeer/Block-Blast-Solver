'use client'

import { FC, useState } from 'react'
import { Button, buttonVariants } from '@/ui/button'
import { FileInput } from '@/ui/file-input'
import example from "public/example.png"
import manualIcon from "public/manual-icon.png"
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import Image from 'next/image'
import tinycolor from 'tinycolor2'


export const metadata = {
  title: 'ImageToAlt - Home',
}

const Page: FC = () => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  // Function to clear the uploaded file
  const clearFile = () => {
    setUploadedFile(null);
    setHideComp((prev) => !prev);
    console.log(hideComp);
    console.log(uploadedFile);
  }

  interface Step {
    board: number[][];
    completedLines: number;
  }

  const [hideComp, setHideComp] = useState(false);
  const [steps, setSteps] = useState<Step[]>([]);
  const [shapeColors, setShapeColors] = useState<Record<string, string>>({});

  // This will receive the steps from FileInput
  const handleUploadSuccess = (
    receivedSteps: Step[],
    receivedShapeColors: Record<string, string>
  ) => {
    setSteps(receivedSteps);
    setShapeColors(receivedShapeColors);
    setHideComp((prev) => !prev);
  };




  function getDynamicStyles(baseColor: string) {
    // Calculate gradient colors
    const lighter = tinycolor(baseColor).lighten(20).toString();
    const darker = tinycolor(baseColor).darken(20).toString();
    const backgroundGradient = `linear-gradient(to bottom right, ${lighter}, ${darker})`;

    // Compute box shadow colors based on base color modifications
    const innerShadow1 = tinycolor(baseColor).saturate(20).setAlpha(0.8).toRgbString();
    const innerShadow2 = tinycolor(baseColor).darken(30).toRgbString();
    const innerShadow3 = tinycolor(baseColor).lighten(40).setAlpha(0.5).toRgbString();

    // Compute border color (a darker variant)
    const borderColor = tinycolor(baseColor).darken(30).toString();

    return {
      background: backgroundGradient,
      boxShadow: `inset 4px 4px 6px ${innerShadow1}, inset -4px -4px 6px ${innerShadow2}, inset 2px 2px 4px ${innerShadow3}, 2px 2px 4px rgba(0, 0, 0, 0.5)`,
      border: `1px solid ${borderColor}`,
    };
  }




  return (
    <section className="container grid items-center lg:gap-20 gap-6 pt-6 pb-8 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        {/* <h1 className="text-3xl font-extrabold leading-tight tracking-tighter sm:text-3xl md:text-5xl lg:text-6xl">
          Block Blast Solver Online
        </h1>
        <p className="max-w-[700px] text-lg text-slate-700 dark:text-slate-400 sm:text-xl">
          Get Block Blast high score solution by taking screenshots
        </p> */}
      </div>





      {/* Try Another Button */}
      {uploadedFile && (
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="flex justify-center w-full my-4">
              <Button
                disabled={!uploadedFile}
                className={buttonVariants({
                  size: "lg",
                  className: "w-fit hover:!bg-[#468beb] hover:!text-white"
                })}
                onClick={clearFile}
              >
                Try Another


                <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-rotate-cw ml-1"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /></svg>


              </Button>
            </div>
          </TooltipTrigger>
          <TooltipContent className="!bg-[#316edf] !text-white">
            <p>Get results for next move</p>
          </TooltipContent>
        </Tooltip>
      )}




      {/* Upload Section */}



      <div className={`${hideComp ? "hidden" : "flex"} flex-col lg:flex-row md:flex-row gap-4 lg:gap-20 justify-center items-stretch bg-[#274aa6] py-8 px-2 lg:p-10 rounded-lg`}>
        {/* Pass uploadedFile state and setter to FileInput */}
        <FileInput uploadedFile={uploadedFile} setUploadedFile={setUploadedFile} onUploadSuccess={handleUploadSuccess} />

        <div className="flex flex-col justify-center items-center gap-4 w-full lg:w-1/2 md:w-1/2 bg-[#0f172d] rounded-lg py-8 px-2 lg:p-10 border-4 border-[#9ac8f6] border-solid">

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




      {uploadedFile && (
        <div className="steps-container-wrapper">
          {steps.map((step, stepIndex) => {
            // Compute completed rows and columns from the board in this step.
            const completedRows = step.board.map((row) => row.every((cell) => cell !== 0));
            const completedColumns = step.board[0].map((_, colIndex) =>
              step.board.every((row) => row[colIndex] !== 0)
            );

            return (
              <div key={stepIndex} className="step-container">
                <p>Step {stepIndex + 1}</p>
                <p>Completed Lines: {step.completedLines}</p>
                <div className="board">
                  {step.board.map((row, rowIndex) => (
                    <div key={rowIndex} className="row">
                      {row.map((cell, cellIndex) => {
                        // Determine the base class for each cell.
                        const cellClass =
                          cell === 0 ? 'empty' : cell === 1 ? 'block' : 'placed';

                        // Default style.
                        let style = {};

                        // Mapping: 2 -> shape 0, 3 -> shape 1, 4 -> shape 2.
                        if (cell === 2) {
                          style = shapeColors?.["shape 0"]
                            ? getDynamicStyles(shapeColors["shape 0"])
                            : { backgroundColor: shapeColors?.["shape 0"] };
                        } else if (cell === 3) {
                          style = shapeColors?.["shape 1"]
                            ? getDynamicStyles(shapeColors["shape 1"])
                            : { backgroundColor: shapeColors?.["shape 1"] };
                        } else if (cell === 4) {
                          style = shapeColors?.["shape 2"]
                            ? getDynamicStyles(shapeColors["shape 2"])
                            : { backgroundColor: shapeColors?.["shape 2"] };
                        }

                        // If the row or the column is complete, add a white border.
                        if (completedRows[rowIndex] || completedColumns[cellIndex]) {
                          style = { ...style, border: "2px solid #4dff00" };
                        }

                        return (
                          <div
                            key={cellIndex}
                            className={`cell ${cellClass}`}
                            style={style}
                          >
                            {/* Optionally render cell content */}
                          </div>
                        );
                      })}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}





      {uploadedFile && (


        <div className="flex flex-col justify-center items-center">
          <p className='text-white text-lg font-bold my-5'>Uploaded Screenshot</p>

          <Image
            src={URL.createObjectURL(uploadedFile)}
            alt="Uploaded Preview"
            width={200}
            height={100}
            className="object-cover rounded-lg mx-auto mb-2 lg:w-1/6 lg:h-[auto] md:w-1/4 sm:w-full md:h-[auto]"
          />
        </div>

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
