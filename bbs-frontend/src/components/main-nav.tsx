import Link from 'next/link'
import { NavItem } from '@/src/types/nav'


import { cn } from '@/lib/utils'
import BlockBlastSolverLogo from "public/block-blast-solver-logo.webp"
import MenuIcon from "public/menu-icon.webp"
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

import { useTab } from '../context/TabContext';
import Image from 'next/image'

interface MainNavProps {
  items?: NavItem[]
}

export function MainNav({ items }: MainNavProps) {

  const { setActiveTab } = useTab();

  return (
    <div className="flex w-full gap-6 md:gap-10 items-center justify-between ">
      <Link href="/" className="hidden float-right items-center space-x-2 md:flex">
     
      <Image
              className="w-10 h-10"
              src={BlockBlastSolverLogo}
              alt="Uploaded Preview"
              width={150}
              height={150}
              loading="lazy"
            />

       
      </Link>
      {items?.length ? (
        <nav className="hidden gap-6 md:flex">
          {items?.map(
            (item, index) =>
              item.href && (
                <Link
                  key={index}
                  href={item.href}
                  className={cn(
                    'flex items-center text-lg font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-100 sm:text-sm',
                    item.disabled && 'cursor-not-allowed opacity-80'
                  )}
                  onClick={() => setActiveTab(prev => prev === 1 ? 2 : 1)}

                >
                  {item.title}
                </Link>
              )
          )}

        </nav>



      ) : null}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            className="-ml-4 text-base hover:bg-transparent focus:ring-0 md:hidden"
          >
            <Image
              className="w-6 h-6"
              src={MenuIcon}
              alt="Uploaded Preview"
              width={150}
              height={150}
              loading="lazy"
            />
         
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          align="start"
          sideOffset={24}
          className="w-[300px] overflow-scroll"
        >
          
          <DropdownMenuSeparator />
          {items?.map(
            (item, index) =>
              item.href && (
                <DropdownMenuItem key={index} asChild>
                  <Link href={item.href} onClick={() => setActiveTab(prev => prev === 1 ? 2 : 1)}>{item.title}</Link>
                </DropdownMenuItem>
              )
          )}
        </DropdownMenuContent>
      </DropdownMenu>
      <Image
              className="w-10 h-10 block md:hidden"
              src={BlockBlastSolverLogo}
              alt="Uploaded Preview"
              width={150}
              height={150}
              loading="lazy"
            />

    </div>
  )
}
