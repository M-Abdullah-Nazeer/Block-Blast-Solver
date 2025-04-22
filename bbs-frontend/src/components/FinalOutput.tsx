import { Step } from "../types/steps"
import tinycolor from 'tinycolor2'

interface FinalOutputProps {
    steps: Step[];
    shapeColors: Record<string, string>;
}
const FinalOutput: React.FC<FinalOutputProps> = ({ steps, shapeColors }) => {


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
                                        // Determine the base classn for each cell.
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

    );
}

export default FinalOutput;