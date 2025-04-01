import os
import pandas as pd
from pathlib import Path

def generate_optimal_parameter_table(input_path, output_path):
    """
    Generate a summary table of optimal parameters from tuning results.
    
    Parameters
    ----------
    input_path : str
        Path to the CSV file containing tuning results
    output_path : str
        Directory where output files will be saved
    """
    # Load data
    results_df = pd.read_csv(input_path)

    # Identify parameter columns
    param_columns = [col for col in results_df.columns if col.startswith('param_')]

    # Collect all rows
    rows = []
    for (config, sample_size, iteration), group in results_df.groupby(['configuration', 'sample_size', 'iteration']):
        row = {
            'configuration': config,
            'sample_size': sample_size,
            'iteration': iteration,
        }
        for param in param_columns:
            param_name = param.replace('param_', '')
            values = group[param]
            if pd.api.types.is_numeric_dtype(values):
                row[param_name] = values.iloc[0]
            else:
                row[param_name] = values.mode().iloc[0] if not values.mode().empty else 'N/A'
        rows.append(row)

    # Create DataFrame
    df_summary = pd.DataFrame(rows)

    # Reorder columns
    ordered_columns = ['configuration', 'sample_size', 'iteration'] + sorted([p.replace('param_', '') for p in param_columns])
    df_summary = df_summary[ordered_columns]

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Save CSV and HTML
    csv_path = os.path.join(output_path, 'optimal_parameters_summary_table.csv')
    html_path = os.path.join(output_path, 'optimal_parameters_summary_table.html')

    df_summary.to_csv(csv_path, index=False)
    df_summary.to_html(html_path, index=False)

    print(f"Table saved to:\n- {csv_path}\n- {html_path}")
    
    return df_summary