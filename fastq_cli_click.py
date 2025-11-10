import argparse
import sys
import json
from fastaq import FastqReader

def main():
    parser = argparse.ArgumentParser(
        description='FASTQ Analyzer - analysis of sequencing data quality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python fastq_cli_argparse.py stats sample.fastq
  python fastq_cli_argparse.py quality sample.fastq --output-prefix my_analysis
  python fastq_cli_argparse.py full-analysis sample.fastq --output-prefix report
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # stats command
    stats_parser = subparsers.add_parser('stats', help='Basic sequence statistics')
    stats_parser.add_argument('fastq_file', help='Input FASTQ file')
    stats_parser.add_argument('--format', choices=['text', 'json'], default='text',
                            help='Output format for statistics')
    
    # quality command
    quality_parser = subparsers.add_parser('quality', help='Sequence quality analysis')
    quality_parser.add_argument('fastq_file', help='Input FASTQ file')
    quality_parser.add_argument('--output-prefix', '-o', default='fastq_quality',
                              help='Prefix for output files')
    
    # content command
    content_parser = subparsers.add_parser('content', help='Nucleotide content analysis')
    content_parser.add_argument('fastq_file', help='Input FASTQ file')
    content_parser.add_argument('--output', default='nucleotide_content.png',
                              help='Output filename')
    
    # full-analysis command
    full_parser = subparsers.add_parser('full-analysis', help='Complete analysis (all plots + statistics)')
    full_parser.add_argument('fastq_file', help='Input FASTQ file')
    full_parser.add_argument('--output-prefix', '-o', required=True,
                           help='Prefix for output files')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'stats':
            handle_stats(args.fastq_file, args.format)
        elif args.command == 'quality':
            handle_quality(args.fastq_file, args.output_prefix)
        elif args.command == 'content':
            handle_content(args.fastq_file, args.output)
        elif args.command == 'full-analysis':
            handle_full_analysis(args.fastq_file, args.output_prefix)
            
    except FileNotFoundError:
        print(f"Error: File {args.fastq_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def handle_stats(fastq_file, format_type):
    """Handler for stats command"""
    print(f"Analyzing statistics for {fastq_file}...")
    
    analyzer = FastqReader(fastq_file)
    count = analyzer.get_sequence_count()
    avg_len = analyzer.get_average_length()
    total_bp = count * avg_len
    
    if format_type == 'json':
        result = {
            "file": fastq_file,
            "sequence_count": count,
            "average_length": round(avg_len, 2),
            "total_bp": round(total_bp, 2)
        }
        print(json.dumps(result, indent=2))
    else:
        print("STATISTICS RESULTS:")
        print(f"  File: {fastq_file}")
        print(f"  Sequence count: {count:,}")
        print(f"  Average length: {avg_len:.2f} bp")
        print(f"  Total data volume: {total_bp:,.0f} bp")

def handle_quality(fastq_file, output_prefix):
    """Handler for quality command"""
    print(f"Quality analysis for {fastq_file}...")
    
    analyzer = FastqReader(fastq_file)
    count = analyzer.get_sequence_count()
    
    print(f"  Processing {count} sequences...")
    
    analyzer.plot_per_base_quality(f"{output_prefix}_per_base_quality.png")
    analyzer.plot_sequence_length_distribution(f"{output_prefix}_length_dist.png")
    
    print("Quality plots saved:")
    print(f"  - {output_prefix}_per_base_quality.png")
    print(f"  - {output_prefix}_length_dist.png")

def handle_content(fastq_file, output_file):
    """Handler for content command"""
    print(f"Nucleotide content analysis for {fastq_file}...")
    
    analyzer = FastqReader(fastq_file)
    analyzer.plot_per_base_content(output_file)
    
    print(f"Content plot saved: {output_file}")

def handle_full_analysis(fastq_file, output_prefix):
    """Handler for full-analysis command"""
    print(f"Complete analysis for {fastq_file}...")
    
    analyzer = FastqReader(fastq_file)
    
    # Statistics
    count = analyzer.get_sequence_count()
    avg_len = analyzer.get_average_length()
    
    print("STATISTICS:")
    print(f"  Sequences: {count:,}")
    print(f"  Average length: {avg_len:.2f} bp")
    print(f"  Total volume: {count * avg_len:,.0f} bp")
    
    # All plots
    print("CREATING PLOTS...")
    analyzer.generate_all_plots()
    
    print("All plots created:")
    print("  - per_base_quality.png")
    print("  - per_base_content.png") 
    print("  - sequence_length_distribution.png")
    
    print(f"Analysis complete. File prefix: {output_prefix}")

if __name__ == "__main__":
    main()