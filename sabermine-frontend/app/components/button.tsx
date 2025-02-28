import { ButtonProps } from "@/app/types";

export function Button({ children, className, ...props }: ButtonProps) {
  return (
    <button className={`px-4 py-2 border border-black rounded-lg ${className}`} {...props}>
      {children}
    </button>
  );
}
