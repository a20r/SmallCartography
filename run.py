
import sys
import carto


def run_master(host, port):
    carto.master.run(host, port)


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        w_type = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]
        if w_type == carto.master.worker.WorkerType.MASTER:
            carto.master.run(host, port)
        elif w_type == carto.master.worker.WorkerType.MAPPER:
            carto.mapper.run(host, port)
        elif w_type == carto.master.worker.WorkerType.REDUCER:
            carto.reducer.run(host, port)
