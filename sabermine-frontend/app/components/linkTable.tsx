import { LinkTableProps } from "@types";
import { Button } from "@components/button";
import React, { useState } from "react";

export function LinkTable({ links }: LinkTableProps) {
    return (
      links.length > 0 && (
        <div className="mt-6 w-full overflow-x-auto">
          <div className="grid grid-cols-2 border-t border-b border-black">
            <div className="p-3 font-bold text-black border-b border-black">Short Link</div>
            <div className="p-3 font-bold text-black border-b border-black">Original Link</div>
            {links.map((link, index) => (
              <React.Fragment key={index}>
                <div key={`${index}-short`} className="p-3 text-black font-medium">{link.short_url}</div>
                <div key={`${index}-original`} className="p-3 text-black">{link.original_url}</div>
              </React.Fragment>
            ))}
          </div>
        </div>
      )
    );
}
