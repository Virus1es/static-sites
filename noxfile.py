import time
import nox

def run_pipeline(session: nox.Session, force: bool = False) -> None:
    """Run experiment analysis and Nikola build."""
    session.install("-r", "requirements.txt")
    
    pipeline_start = time.perf_counter()

    analysis_start = time.perf_counter()
    
    analyze_args = [
        "python",
        "-m",
        "scripts.analyze",
    ]
    
    if force:
        analyze_args.append("--force")
    
    session.run(*analyze_args)
    
    analysis_time = time.perf_counter() - analysis_start
    
    build_start = time.perf_counter()    
    session.run("nikola", "build")
    nikola_time = time.perf_counter() - build_start
    
    pipeline_time = time.perf_counter() - pipeline_start
    
    print("\n" + "=" * 50)
    print("PIPELINE TIMING")
    print("=" * 50)
    print(f"Analysis time: {analysis_time:.3f} s")
    print(f"Nikola build time: {nikola_time:.3f} s")
    print(f"Pipeline time: {pipeline_time:.3f} s")
    print("=" * 50)

@nox.session
def build(session: nox.Session) -> None:
    """Run cached pipeline."""
    run_pipeline(session)

@nox.session
def build_force(session: nox.Session) -> None:
    """Run pipeline with forced experiment recalculation."""
    run_pipeline(session, force=True)