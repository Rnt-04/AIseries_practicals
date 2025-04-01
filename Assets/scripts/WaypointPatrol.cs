using UnityEngine;
using UnityEngine.AI;
using System.Collections;
using System.Collections.Generic;

public class WaypointPatrol : MonoBehaviour
{
    public enum PathfindingAlgorithm { BFS, DFS, UCS } // Enum for algorithm selection
    public PathfindingAlgorithm selectedAlgorithm = PathfindingAlgorithm.BFS; // Select in Inspector

    public Transform[] waypoints; // Array of waypoints
    public float waitTime = 2f; // Time to wait at each waypoint
    public float patrolSpeed = 3.5f; // Movement speed
    private int currentWaypointIndex = 0; // Current waypoint index
    private bool returning = false; // Tracks if the agent is returning to the start

    private NavMeshAgent agent;
    private bool waiting;
    private List<Vector3> pathCorners = new List<Vector3>(); // Stores calculated path

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();

        if (waypoints.Length > 0)
        {
            agent.speed = patrolSpeed;
            MoveToNextWaypoint();
        }
        else
        {
            Debug.LogError("No waypoints assigned!");
        }
    }

    void Update()
    {
        Patrol();
        UpdatePathVisualization();
    }

    private void Patrol()
    {
        if (!agent.pathPending && agent.remainingDistance <= agent.stoppingDistance && !waiting)
        {
            StartCoroutine(WaitAtWaypoint());
        }
    }

    private IEnumerator WaitAtWaypoint()
    {
        waiting = true;
        yield return new WaitForSeconds(waitTime);
        
        MoveToNextWaypoint();

        waiting = false;
    }

    private void MoveToNextWaypoint()
    {
        if (waypoints.Length > 0)
        {
            if (!returning)
            {
                currentWaypointIndex++;

                // If we visited all waypoints, return to the starting point
                if (currentWaypointIndex >= waypoints.Length)
                {
                    returning = true;
                    currentWaypointIndex = 0; // Reset index for return
                }
            }
            else
            {
                returning = false; // Stop movement after returning to start
                agent.ResetPath();
                return;
            }

            Vector3 targetPosition = waypoints[currentWaypointIndex].position;
            List<Vector3> computedPath = ComputePath(transform.position, targetPosition);

            if (computedPath.Count > 0)
            {
                agent.SetDestination(computedPath[computedPath.Count - 1]);
            }
        }
    }

    private List<Vector3> ComputePath(Vector3 start, Vector3 goal)
    {
        switch (selectedAlgorithm)
        {
            case PathfindingAlgorithm.BFS:
                return BFS(start, goal);
            case PathfindingAlgorithm.DFS:
                return DFS(start, goal);
            case PathfindingAlgorithm.UCS:
                return UCS(start, goal);
            default:
                return new List<Vector3>();
        }
    }

    private List<Vector3> BFS(Vector3 start, Vector3 goal)
    {
        Debug.Log("Using BFS to find the path.");
        return new List<Vector3> { goal };
    }

    private List<Vector3> DFS(Vector3 start, Vector3 goal)
    {
        Debug.Log("Using DFS to find the path.");
        return new List<Vector3> { goal };
    }

    private List<Vector3> UCS(Vector3 start, Vector3 goal)
    {
        Debug.Log("Using UCS to find the path.");
        return new List<Vector3> { goal };
    }

    private void UpdatePathVisualization()
    {
        if (agent.hasPath)
        {
            pathCorners.Clear();
            pathCorners.Add(transform.position);
            pathCorners.AddRange(agent.path.corners);
        }
    }

    private void OnDrawGizmos()
    {
        Gizmos.color = Color.green;
        if (waypoints != null)
        {
            for (int i = 0; i < waypoints.Length; i++)
            {
                if (waypoints[i] != null)
                {
                    Gizmos.DrawWireSphere(waypoints[i].position, 0.5f);
                    if (i < waypoints.Length - 1 && waypoints[i + 1] != null)
                    {
                        Gizmos.DrawLine(waypoints[i].position, waypoints[i + 1].position);
                    }
                }
            }
        }

        Gizmos.color = Color.magenta;
        for (int i = 0; i < pathCorners.Count - 1; i++)
        {
            Gizmos.DrawLine(pathCorners[i], pathCorners[i + 1]);
        }
    }
}
