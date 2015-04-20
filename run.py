
import carto
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Runs programs for the carto MapReduce library"
    )

    parser.add_argument(
        "--host", dest="host", type=str, default="localhost",
        help="Host of the program"
    )

    parser.add_argument(
        "--port", dest="port", type=int, default=8000,
        help="Port of the program"
    )

    parser.add_argument(
        "--name", dest="name", type=str,
        help="Name used by the worker"
    )

    parser.add_argument(
        "--program", dest="program", type=str, default="client",
        help="Used to determine what program will run"
    )

    parser.add_argument(
        "--ns-host", dest="ns_host", type=str, default="localhost",
        help="Host of the name server"
    )

    parser.add_argument(
        "--ns-port", dest="ns_port", type=int, default="8080",
        help="Port used by the name server"
    )

    args = parser.parse_args()

    if args.program == carto.master.worker.WorkerType.MASTER:
        carto.master.run(args.host, args.port)
    elif args.program == carto.master.worker.WorkerType.MAPPER:
        carto.mapper.run(args.host, args.port, args.ns_host,
                         args.ns_port, args.name)
    elif args.program == carto.master.worker.WorkerType.REDUCER:
        carto.reducer.run(args.host, args.port, args.ns_host,
                          args.ns_port, args.name)


if __name__ == "__main__":
    main()
