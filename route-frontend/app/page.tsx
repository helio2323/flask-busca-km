"use client"

import { useState } from "react"
import { Sidebar } from "@/components/sidebar"
import { RouteCalculator } from "@/components/route-calculator"
import { RouteHistory } from "@/components/route-history"
import { Dashboard } from "@/components/dashboard"
import { GroupManager } from "@/components/group-manager"

export default function HomePage() {
  const [activeSection, setActiveSection] = useState<"dashboard" | "calculator" | "history" | "groups">(
    "dashboard",
  )

  const renderContent = () => {
    switch (activeSection) {
      case "dashboard":
        return <Dashboard />
      case "calculator":
        return <RouteCalculator />
      case "history":
        return <RouteHistory />
      case "groups":
        return <GroupManager />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar activeSection={activeSection} onSectionChange={setActiveSection} />
      <main className="flex-1 overflow-hidden">{renderContent()}</main>
    </div>
  )
}
