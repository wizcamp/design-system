# Color Sync

Process to harvest color tokens - placing them in `guidelines/colors.md` for now - from the Design Systems page to feed both the guidelines (design system) infrastructure, but also the codebase by converting RGB to OKLCH values and then generating a barebones `globals.css`.  This can be augmented and refined to update the actual `globals.css` (master Tailwind stylesheets) to generate a true design-to-code pipeline that keeps things in sync (necessary because these critical color tokes exist in 5 locations).

```mermaid
graph TD
    %% Define the stages and data flow

    A[Start: Receive Task Prompt] --> B{Step 1: Preparation};
    B --> C[Step 2: Extraction];
    C --> D{Figma MCP: Get Variable Definitions};
    D --> E[Hex Color for all themes];
    E --> F{Step 3: Transformation};
    F --> G[Python Script: RGB -> OKLCH Conversion];
    G --> H[OKLCH Color Data];
    H --> I{Step 4: Documentation};
    I --> J[Filesystem MCP: Write to colors.md];
    J --> K{Step 5: CSS Implementation};
    K --> L[Filesystem MCP: Write to globals.css];
    L --> Z[End: Deliver Design System Assets];

    %% Styling for clarity
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style Z fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#ccf,stroke:#333
    style C fill:#ccf,stroke:#333
    style F fill:#ccf,stroke:#333
    style I fill:#ccf,stroke:#333
    style K fill:#ccf,stroke:#333

    %% Annotations
    subgraph Input/Tooling
        D
        G
        J
        L
    end

    subgraph Data Flow
        E
        H
    end

    %% Describe the process details in notes
    click B "Action: Use embedded Python script for conversions."
    click C "Action: Call get_variable_defs on Figma node (21275-9)."
    click F "Action: Iterate and apply RGB_to_OKLCH function."
    click I "Action: Format results into GFM table structure."
    click K "Action: Structure CSS, injecting variables and template blocks."
    ```

# Card vs. Section 

A card is a visually bounded container—typically  styled with borders, backgrounds, or shadows—best used to represent a distinct, portable object, whereas a section relies on open whitespace and typography to group related content within the continuous vertical flow of a page.

https://share.gemini.google/jYnmRkKyaxMI
