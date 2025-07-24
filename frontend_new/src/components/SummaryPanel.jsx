import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

const SummaryPanel = ({ summary }) => {
  if (!summary) return null;

  return (
    <Card className="w-full bg-gray-50 rounded-2xl shadow-sm mt-2 p-4">
      <CardContent>
        <h3 className="text-lg font-semibold mb-2">🧠 AI Summary</h3>
        <ScrollArea className="h-32 pr-2">
          <p className="text-sm text-muted-foreground whitespace-pre-wrap">
            {summary}
          </p>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default SummaryPanel;
