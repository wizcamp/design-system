'use client';

import { Chrome, Github, LogOut } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { SettingsSection } from './settings-section';
import type { AuthUser } from '@wizcamp/api-contract/lms';

type IdentitySectionProps = {
  user: AuthUser | null | undefined;
  onSignOut: () => void;
};

export function IdentitySection({ user, onSignOut }: IdentitySectionProps) {
  const initials = user
    ? `${user.firstName?.[0] ?? ''}${user.lastName?.[0] ?? ''}`.toUpperCase()
    : '?';

  return (
    <SettingsSection title="Account">
      <div className="flex items-center gap-4">
        <Avatar className="size-16">
          <AvatarImage src={user?.avatarUrl ?? ''} alt={user?.firstName ?? ''} />
          <AvatarFallback className="text-lg">{initials}</AvatarFallback>
        </Avatar>
        <div>
          <p className="font-semibold">{user?.firstName} {user?.lastName}</p>
          <p className="text-muted-foreground text-sm">{user?.email}</p>
          {user?.oauthProvider && (
            <p className="text-muted-foreground mt-0.5 flex items-center gap-1 text-xs">
              {user.oauthProvider === 'google'
                ? <Chrome className="size-3" />
                : <Github className="size-3" />}
              Connected via {user.oauthProvider === 'google' ? 'Google' : 'GitHub'}
            </p>
          )}
        </div>
      </div>
      <Separator />
      <Button variant="outline" size="sm" onClick={onSignOut}>
        <LogOut className="mr-2 size-4" />Sign out
      </Button>
    </SettingsSection>
  );
}
