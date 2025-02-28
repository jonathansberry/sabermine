import { ReactNode } from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    children: ReactNode;
}

export type LinkCreatorProps = {
    text: string;
    setText: (text: string) => void;
    onDrop: (files: File[]) => void;
    onCreate: () => void;
};

export type LinkTableProps = {
    links: { short_url: string; original_url: string }[];
};
