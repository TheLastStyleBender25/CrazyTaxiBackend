from sqlalchemy.orm import Session
from starlette import status
from fastapi import Depends, HTTPException
from app.models import PlayerClaimedMilestone, RideMilestone, Player
from app.core.logger import logger

def claim_milestone(db, player, milestone_id):
    existing = db.query(PlayerClaimedMilestone).filter(PlayerClaimedMilestone.player_id==player.id, PlayerClaimedMilestone.milestone_id == milestone_id).first()
    if existing:
        logger.error(f"milestone {milestone_id} already claimed")
        raise ValueError("already claimed")
    milestone = db.query(RideMilestone).filter(RideMilestone.id == milestone_id).first()
    if (player.total_rides_completed < milestone.required_rides):
        logger.error(f"not enough rides")
        raise ValueError("not enough rides")
    player.gems += milestone.gem_reward
    claim = PlayerClaimedMilestone(player_id=player.id, milestone_id=milestone.id)

    db.add(claim)
    db.commit()

    return {

        "message":
            "Milestone claimed",

        "gems":
            player.gems,

        "reward":
            milestone.gem_reward
    }

def get_claimable_milestones(db, player):
    claimed = db.query(PlayerClaimedMilestone).filter(PlayerClaimedMilestone.player_id==player.id).all()
    claimed_ids = set()
    for c in claimed:
        claimed_ids.add(c.milestone_id)
    milestones = db.query(RideMilestone).all()
    claimable = []
    for milestone in milestones:
        if (milestone.id not in claimed_ids):
            claimable.append({ "id": milestone.id, "required_rides": milestone.required_rides, "gem_reward": milestone.gem_reward})

    return {"claimable": claimable, "milestones": milestones}
