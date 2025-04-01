using UnityEngine;
using UnityEngine.AI;
using System.Collections;
using System.Collections.Generic;

public class PathFinder : MonoBehaviour
{
    public Transform[] waypoints; // Array of waypoints for patrol
    public float waitTime = 2f; // Time to wait at each waypoint
    public float patrolSpeed = 3.5f; // Speed of the patrol agent
    private int currentWaypointIndex = 0; // Current waypoint index

    private NavMeshAgent agent;
    private bool waiting;
    private List<Vector3> pathCorners = new List<Vector3>(); // Stores the calculated path

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
        
        // Move to the next waypoint
        MoveToNextWaypoint();

        waiting = false;
    }

    private void MoveToNextWaypoint()
    {
        if (waypoints.Length > 0)
        {
            currentWaypointIndex = (currentWaypointIndex + 1) % waypoints.Length;
            agent.SetDestination(waypoints[currentWaypointIndex].position);
        }
    }

    private void UpdatePathVisualization()
    {
        if (agent.hasPath)
        {
            pathCorners.Clear();
            pathCorners.Add(transform.position); // Start position
            pathCorners.AddRange(agent.path.corners);
        }
    }

    private void OnDrawGizmos()
    {
        // Draw waypoints
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

        // Draw actual path being taken
        Gizmos.color = Color.magenta; // Changed color for better visibility
        for (int i = 0; i < pathCorners.Count - 1; i++)
        {
            Gizmos.DrawLine(pathCorners[i], pathCorners[i + 1]);
        }
    }
}
