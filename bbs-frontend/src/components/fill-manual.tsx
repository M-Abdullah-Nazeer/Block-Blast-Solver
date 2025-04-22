"use client";

import React, { useState } from "react";
import axios from "axios";

import { useTab } from '../context/TabContext';

interface FillManualProps {
    handleUploadSuccess: (
      receivedSteps: any[], // Update with your Step type
      receivedShapeColors: Record<string, string>
    ) => void;
    // ... other props if needed
  }
const GRID_SIZE = 8;

type GridType = number[][];

const createEmptyGrid = (): GridType =>
  Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));
const createEmptyShape1 = (): GridType =>
  Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));
const createEmptyShape2 = (): GridType =>
  Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));
const createEmptyShape3 = (): GridType =>
  Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));

const FillManual: React.FC<FillManualProps> = ({ handleUploadSuccess }) => {
  const [grid, setGrid] = useState<GridType>(createEmptyGrid());
  const [shape1, setShape1] = useState<GridType>(createEmptyShape1());
  const [shape2, setShape2] = useState<GridType>(createEmptyShape2());
  const [shape3, setShape3] = useState<GridType>(createEmptyShape3());
  const { setActiveTab  } = useTab();

  const API_URL ="http://localhost:8000";

 

  const handleClick = (rowIdx: number, colIdx: number): void => {
    setGrid((prevGrid) =>
      prevGrid.map((row, rIdx) =>
        row.map((cell, cIdx) =>
          rIdx === rowIdx && cIdx === colIdx ? 1 : cell
        )
      )
    );
  };
  const handleShape1 = (rowIdx: number, colIdx: number): void => {
    setShape1((prevGrid) =>
      prevGrid.map((row, rIdx) =>
        row.map((cell, cIdx) =>
          rIdx === rowIdx && cIdx === colIdx ? 1 : cell
        )
      )
    );
  };
  const handleShape2 = (rowIdx: number, colIdx: number): void => {
    setShape2((prevGrid) =>
      prevGrid.map((row, rIdx) =>
        row.map((cell, cIdx) =>
          rIdx === rowIdx && cIdx === colIdx ? 1 : cell
        )
      )
    );
  };
  const handleShape3 = (rowIdx: number, colIdx: number): void => {
    setShape3((prevGrid) =>
      prevGrid.map((row, rIdx) =>
        row.map((cell, cIdx) =>
          rIdx === rowIdx && cIdx === colIdx ? 1 : cell
        )
      )
    );
  };

  const handleClear = (): void => {
    setGrid(createEmptyGrid());
    setShape1(createEmptyGrid());
    setShape2(createEmptyGrid());
    setShape3(createEmptyGrid());
   
  };







  const handleSolve = async (): Promise<void> => {
    try {
        const payload = {
            grid: grid,
            shape1: shape1,
            shape2: shape2,
            shape3: shape3,
        };

        const response = await axios.post(
          `${API_URL}/fm`, 
            payload,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        console.log("Stepwise boards:", response.data.final_output);
        setActiveTab(3); 

        handleUploadSuccess(
            response.data.final_output,  // Steps data
            response.data.shape_colors   // Shape colors
          );
        
    } catch (error) {
      // alert(`Backend URL: ${API_URL}`); 
        console.error("Error solving puzzle:", error);
        // Handle error state
    }
};


  return (

<>

    <div className="flex flex-col justify-center items-center">

<p className="text-lg font-bold text-white text-center mb-6">Fill the grid blocks</p>

      <div style={{ display: "inline-block" }}>
        {grid.map((row, rowIdx) => (
          <div key={rowIdx} style={{ display: "flex" }}>
            {row.map((cell, colIdx) => (
              <div
                key={colIdx}
                onClick={() => handleClick(rowIdx, colIdx)}
                className="fm-grid"
                style={{
                 
                  backgroundColor: cell ? "#00bfff" : "#f0f2ff",
                  border: "1px solid #ccc",
                  margin: "1px",
                  cursor: "pointer",
                  transition: "0.2s",
                }}
              />
            ))}
          </div>
        ))}
      </div>

      {/* <pre style={{ marginTop: "20px", fontSize: "14px" }}>
        {JSON.stringify(grid, null, 2)}
      </pre> */}
    </div>


    <div className="flex flex-col justify-center items-center">

<p className="text-lg font-bold text-white  mb-2 mt-6 lg:mt-0 ">Fill the 3 shapes</p>

<div   className="py-6 grid  grid-cols-1 lg:grid-cols-[1fr_1fr_1fr] items-center justify-center gap-4 md:gap-[20px] lg:gap-[20px] xl:gap-[20px]">

      <div style={{ display: "inline-block" }}>
      <p className="mb-2 text-base leading-7 text-gray-300 text-center">Shape 1</p>
        {shape1.map((row, rowIdx) => (
          <div key={rowIdx} style={{ display: "flex" }}>
            {row.map((cell, colIdx) => (
              <div
                key={colIdx}
                onClick={() => handleShape1(rowIdx, colIdx)}
                className="fm-block"
                style={{
                    backgroundColor: cell ? "#00bfff" : "#f0f2ff",
                  transition: "0.2s",
                }}
              />
            ))}
          </div>
        ))}
      </div>

      <div style={{ display: "inline-block" }}>
      <p className="mb-2 text-base leading-7 text-gray-300 text-center">Shape 2</p>
        {shape2.map((row, rowIdx) => (
          <div key={rowIdx} style={{ display: "flex" }}>
            {row.map((cell, colIdx) => (
              <div
                key={colIdx}
                onClick={() => handleShape2(rowIdx, colIdx)}
                className="fm-block"
                style={{
               
                  backgroundColor: cell ? "#00bfff" : "#f0f2ff",
               
                  transition: "0.2s",
                }}
              />
            ))}
          </div>
        ))}
      </div>


      <div style={{ display: "inline-block" }}>

        <p className="mb-2 text-base leading-7 text-gray-300 text-center">Shape 3</p>
        {shape3.map((row, rowIdx) => (
          <div key={rowIdx} style={{ display: "flex" }}>
            {row.map((cell, colIdx) => (
              <div
                key={colIdx}
                onClick={() => handleShape3(rowIdx, colIdx)}
                className="fm-block"
                style={{
              
                  backgroundColor: cell ? "#00bfff" : "#f0f2ff",
             
         
                  transition: "0.2s",
                }}
              />
            ))}
          </div>
        ))}
      </div>

    
    </div>

<div className="flex flex-col lg:flex-row items-center justify-center">

    <button className="flex mr-0 mb-2 lg:mb-0 lg:mr-2 items-center justify-center gap-3 bg-transparent border border-solid border-white text-white p-[16px] lg:px-[16px] lg:py-[16px] rounded-lg hover:bg-[#00bfff20] transition-all duration-300 ease-in-out w-[200px] lg:w-[150px] h-[56px] cursor-pointer" onClick={handleClear}>
              {/* <Image alt="select image" className="w-[32px] h-[32px] aspect-square" src={manualIcon} /> */}
              <span className="text-18px font-semibold leading-24px text-center">Clear</span>
            </button>
    <button className="flex ml-0 mt-2 lg:mt-0 lg:ml-2 items-center justify-center gap-3 bg-[#0088cc] active:bg-[#0088cc5c] text-white p-[16px] lg:px-[24px] lg:py-[16px] rounded-lg hover:bg-[#00bfff] transition-all duration-300 ease-in-out w-[200px] lg:w-[150px] h-[56px] cursor-pointer"  onClick={handleSolve}>
              {/* <Image alt="select image" className="w-[32px] h-[32px] aspect-square" src={manualIcon} /> */}
              <span className="text-18px font-semibold leading-24px text-center">Solve</span>
            </button>

            </div>

    </div>


  

    </>

  );
};

export default FillManual;
