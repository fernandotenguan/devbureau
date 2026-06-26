'use client';

import { Button } from '@/components/ui/button';
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Heart } from 'lucide-react';

interface DonateDialogProps {
    className?: string;
}

export default function DonateDialog({ className }: DonateDialogProps) {
    return (
        <Dialog>
            <DialogTrigger render={<Button variant="outline" className={className} />}>
                <Heart className="w-3 h-3 mr-1.5 text-red-500" />
                Donate
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <span>Support DevBureau</span>
                    </DialogTitle>
                    <DialogDescription className="space-y-2 pt-2">
                        DevBureau is built and maintained independently. If it saves you time, consider supporting its development via PIX.
                    </DialogDescription>
                </DialogHeader>

                <div className="p-4 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50">
                    <div className="flex flex-col items-center gap-4">
                        <img className="w-48 h-48 rounded-lg" src="/pix-fernando.png" alt="PIX QR Code" />
                        <div className="text-center space-y-1">
                            <div className="text-sm font-medium text-zinc-900 dark:text-zinc-50">
                                PIX key: <span className="font-mono">fernando.tenguan@gmail.com</span>
                            </div>
                        </div>
                    </div>
                </div>

                <DialogFooter>
                    <DialogClose render={<Button variant="ghost" />}>
                        Close
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
