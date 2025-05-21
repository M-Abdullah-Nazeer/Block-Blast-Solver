import OGImage from "public/og-image.webp"
import HomePageComponent from "../components/HomePageComponent";
import { FC } from 'react'





// app/page.tsx (Homepage)
export const metadata = {
  // Basic SEO
  title: "Block Blast Solver | Free Online AI Screenshot Solver",
  description: "Get Block Blast high score in 1 click. Upload screenshot and let our AI solver give you step-by-step solution. Enjoy free unlimited attempts.",

  // alternates: {
  //   canonical: "https://blockblastsolverai.com", // Direct string declaration
  // },
  // Open Graph (Social Sharing)
  openGraph: {
    title: "Block Blast Solver - Instant Puzzle Solutions",
    description: "AI-powered tool that analyzes Block Blast screenshots to generate optimal moves",
    url: "https://blockblastsolverai.com",
    type: "website",
    images: [{
      url: OGImage,
      width: 1076,
      height: 428,
      alt: "AI Block Blast cheat",
    }],
  },

  // Twitter Card
  twitter: {
    card: "summary_large_image",
    title: "Block Blast Solver AI",
    description: "Free AI-powered solution generator for Block Blast puzzles",
    images: [{  // Wrap in array with object
      url: OGImage,
      width: 1076,
      height: 428,
      alt: "AI Block Blast cheat",
    }]
  },
};




const Page: FC = () => {
  
  return (

 


<HomePageComponent/>




  )
}

export default Page
