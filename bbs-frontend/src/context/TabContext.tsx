'use client';
import { createContext, useContext, useState, ReactNode, Dispatch, SetStateAction } from 'react';

type TabContextType = {
  activeTab: 1 | 2;
  setActiveTab: Dispatch<SetStateAction<1 | 2>>;
};

const TabContext = createContext<TabContextType | undefined>(undefined);

export function TabProvider({ children }: { children: ReactNode }) {
  const [activeTab, setActiveTab] = useState<1 | 2>(1);
  
  return (
    <TabContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabContext.Provider>
  );
}

export function useTab() {
  const context = useContext(TabContext);
  if (context === undefined) {
    throw new Error('useTab must be used within a TabProvider');
  }
  return context;
}